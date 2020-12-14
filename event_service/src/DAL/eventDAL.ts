import * as _ from 'lodash';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { getDb } from '@src/DAL/setup';
import { CreateEventRequest } from '@src/DTO/createEventRequest';
import { CreateRecurringEventRequest } from '@src/DTO/createRecurringEventRequest';

const DEFAULT_LIMIT = 25;
const MILES_TO_METERS = 1609.34;
const makeVector = `to_tsvector(org.name || '' || event.title || ' ' || event.description)`;

const db = getDb('events');
/**
 * Middleware for processing a raw event object to event response objects?
 */
export class EventDAL {
  async getEvents(
    query: GetEventsRequest,
    geocode: GetGeocodeResponse,
  ): Promise<any> {
    let result = await this.queryEvents(
      db('events.event as event')
        .select(
          'event.id',
          'event.title',
          'event.url',
          'event.description',
          'org.name as organization_name',
          'event.price',
          'event.startTime',
          'event.endTime',
          'event.category',
          'event.createdDate',
          'geo.address',
          'geo.lat',
          'geo.lon',
          'geo.neighborhood',
        )
        .select(
          db.raw(
            `${
              query.keywords ? `ts_rank_cd(${makeVector}, to_tsquery(?))` : '?'
            } as rank`,
            query.keywords ? query.keywords : 0,
          ),
        ),
      query,
      geocode,
    )
      .offset(query.offset || 0)
      .limit(query.limit || DEFAULT_LIMIT)
      .orderBy('rank', 'desc')
      .orderBy('event.startTime', 'asc');

    const resultCount = await this.queryEvents(
      db('events.event as event').count('*'),
      query,
      geocode,
    ).first();

    return { totalCount: resultCount.count, events: result };
  }

  async createEvents(
    data: CreateEventRequest,
    orgId: number,
    geocodeId: number,
  ): Promise<void> {
    await db('events.event').insert({
      title: data.title,
      url: data.url,
      description: data.description,
      organizationId: orgId,
      price: data.price,
      geocodeId: geocodeId,
      startTime: data.eventTime.startTimestamp,
      endTime: data.eventTime.endTimestamp,
    });
  }

  // async deleteEvents(organizations: string[]): Promise<any> {
  //   const val = await db('events.event')
  //     .whereIn('organization', organizations)
  //     .del();
  //   return val;
  // }

  async nullifyGeocodeIds() {
    await db('events.event').update('geocodeId', null);
  }

  async deleteAllEvents() {
    await db('events.event').del();
  }

  async cleanupEvents() {
    await db('events.event').where('end_time', '<', new Date()).del();
  }

  async createMonthlyRecurringEvent(
    weekday: string | null,
    weekNumber: number | null,
    dayOfMonth: number | null,
  ): Promise<number> {
    let scheduleIds = await db('events.monthly_recurring_schedule')
      .insert({ weekday, weekNumber, dayOfMonth })
      .returning('id');
    return scheduleIds[0];
  }

  async createRecurringEvent(
    data: CreateRecurringEventRequest,
    orgId: number,
    geocodeId: number,
    monthlyScheduleId: number | null,
  ): Promise<number> {
    let ids = await db('events.recurring_event')
      .insert({
        title: data.title,
        url: data.url,
        description: data.description,
        organizationId: orgId,
        price: data.price,
        geocodeId: geocodeId,
        startTime: data.eventTime.startTimestamp,
        endTime: data.eventTime.endTimestamp,
        requiresPhysicalActivities: data.requiresPhysicalActivities,
        handicapAccessible: data.isHandicapAccessible,
        monthlyRecurringScheduleId: monthlyScheduleId,
      })
      .returning('id');

    return ids[0];
  }

  async createWeeklyRecurringSchedules(scheduleId: number, weekdays: string[]) {
    await db('events.weekly_recurring_schedule_day').insert(
      weekdays.map((d) => ({
        recurringEventId: scheduleId,
        weekday: d,
      })),
    );
  }

  async getOrgId(orgName: string): Promise<number> {
    let orgs = await db('events.organization as org')
      .select('org.id')
      .where('org.name', orgName);

    if (orgs.length === 0) {
      let newIds = await db('events.organization as org')
        .insert({
          name: orgName,
        })
        .returning('id');
      return newIds[0].id;
    } else {
      return orgs[0].id;
    }
  }

  private queryEvents(
    selectFunc: any,
    query: GetEventsRequest,
    geocode: GetGeocodeResponse,
  ) {
    const res = selectFunc
      .innerJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
      .innerJoin(
        'events.organization as org',
        'event.organization_id',
        'org.id',
      )
      .where('event.startTime', '>=', query.startTime || '01-01-1970')
      .andWhere('event.endTime', '<=', query.endTime || '12-31-2099')
      .modify((queryBuilder) => {
        if (geocode) {
          queryBuilder
            .whereNotNull('geo.lat')
            .whereNotNull('geo.lon')
            .andWhere('geo.lat', '!=', 'NaN')
            .andWhere('geo.lon', '!=', 'NaN')
            .andWhereRaw(
              'earth_distance(ll_to_earth(geo.lat, geo.lon), ll_to_earth(?, ?)) <= ?',
              [geocode.lat, geocode.lon, query.miles * MILES_TO_METERS],
            );
        }

        if (query.neighborhood) {
          queryBuilder.andWhere('geo.neighborhood', '=', query.neighborhood);
        }
        if (query.keywords) {
          queryBuilder.andWhereRaw(
            `${makeVector} @@ to_tsquery(?)`,
            query.keywords,
          );
        }
      });
    return res;
  }
}
