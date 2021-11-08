import * as _ from 'lodash';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { getDb } from '@src/DAL/setup';
import { CreateEventRequest } from '@src/DTO/createEventRequest';
import { CreateRecurringEventRequest } from '@src/DTO/createRecurringEventRequest';
import { UpdateEventRequest } from '@src/DTO/updateEventRequest';

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
          'org.name as organizationName',
          'event.price',
          'event.startTime',
          'event.endTime',
          'event.createdDate',
          'event.requiresPhysicalActivities',
          'event.handicapAccessible',
          'event.recurringEventId',
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

  async createEvent(
    data: CreateEventRequest,
    orgId: number,
    authorId: number,
    geocodeId: number,
  ): Promise<void> {
    await db('events.event').insert({
      title: data.title,
      url: data.url,
      description: data.description,
      organizationId: orgId,
      authorId,
      price: data.price,
      geocodeId: geocodeId,
      startTime: data.eventTime.startTimestamp,
      endTime: data.eventTime.endTimestamp,
      handicapAccessible: data.handicapAccessible,
      requiresPhysicalActivities: data.requiresPhysicalActivities,
    });
  }
  // TODO somersbmatthews : change event request to update event request
  async updateEvent(
    data: UpdateEventRequest,
    orgId: number,
    authorId: number,
    geocodeId: number,
  ): Promise<void> {
    await db('events.event').where('id', '=', data.id).update({
      title: data.title,
      url: data.url,
      description: data.description,
      organizationId: orgId,
      authorId,
      price: data.price,
      geocodeId: geocodeId,
      startTime: data.eventTime.startTimestamp,
      endTime: data.eventTime.endTimestamp,
      handicapAccessible: data.handicapAccessible,
      requiresPhysicalActivities: data.requiresPhysicalActivities,
    });
  }

  // TODO somersbmatthews : add and finish updateEvents method

  async updateEvents(
    data: UpdateEventRequest,
    orgId: number,
    authorId: number,
    geocodeId: number,
  ): Promise<void> {
    await db('events.event').insert({
      title: data.title,
      url: data.url,
      description: data.description,
      organizationId: orgId,
      authorId,
      price: data.price,
      geocodeId: geocodeId,
      startTime: data.eventTime.startTimestamp,
      endTime: data.eventTime.endTimestamp,
      handicapAccessible: data.handicapAccessible,
      requiresPhysicalActivities: data.requiresPhysicalActivities,
    });
  }

  async createEvents(data: any[]): Promise<void> {
    const { sql, bindings } = db('events.event')
      .insert(
        data.map((d) => ({
          title: d.title,
          url: d.url,
          description: d.description,
          organizationId: d.organizationId,
          authorId: d.authorId,
          price: d.price,
          geocodeId: d.geocodeId,
          startTime: d.startTime,
          endTime: d.endTime,
          recurringEventId: d.id,
          handicapAccessible: d.handicapAccessible,
          requiresPhysicalActivities: d.requiresPhysicalActivities,
        })),
      )
      .toSQL();

    await db.raw(`${sql} on conflict do nothing`, bindings);
  }

  async nullifyGeocodeIds() {
    await db('events.event').update('geocodeId', null);
  }

  async cleanupEvents() {
    await db('events.event').where('end_time', '<', new Date()).del();
  }

  async createMonthlyRecurringEvent(
    recurringEventId: number,
    weekday: string | null,
    weekNumber: number | null,
    dayOfMonth: number | null,
  ) {
    await db('events.monthly_recurring_schedule').insert({
      recurringEventId,
      weekday,
      weekNumber,
      dayOfMonth,
    });
  }

  async createWeeklyRecurringSchedules(scheduleId: number, weekdays: string[]) {
    await db('events.weekly_recurring_schedule').insert(
      weekdays.map((d) => ({
        recurringEventId: scheduleId,
        weekday: d,
      })),
    );
  }

  async createRecurringEvent(
    data: CreateRecurringEventRequest,
    orgId: number,
    authorId: number,
    geocodeId: number,
  ): Promise<number> {
    let ids = await db('events.recurring_event')
      .insert({
        title: data.title,
        url: data.url,
        description: data.description,
        organizationId: orgId,
        authorId,
        price: data.price,
        geocodeId: geocodeId,
        startTime: data.eventTime.startTimestamp,
        endTime: data.eventTime.endTimestamp,
        requiresPhysicalActivities: data.requiresPhysicalActivities,
        handicapAccessible: data.handicapAccessible,
      })
      .returning('id');

    return ids[0];
  }

  async getOrgId(orgName: string): Promise<number> {
    return await this.getIdFromName(orgName, 'organization');
  }

  async getAuthorId(authorName: string): Promise<number> {
    return await this.getIdFromName(authorName, 'author');
  }

  private async getIdFromName(name: string, table: string) {
    const tableExpr = `events.${table} as t`;
    let entries = await db(tableExpr).select('t.id').where('t.name', name);

    if (entries.length === 0) {
      let newIds = await db(tableExpr)
        .insert({
          name,
        })
        .returning('id');

      return newIds[0];
    } else {
      return entries[0].id;
    }
  }

  async getWeeklyRecurringSchedules(scheduleId: number | undefined) {
    let query = db('events.recurring_event as re')
      .select(
        're.id',
        're.title',
        're.url',
        're.description',
        're.price',
        're.geocodeId',
        're.organizationId',
        're.authorId',
        're.startTime',
        're.endTime',
        're.requiresPhysicalActivities',
        're.handicapAccessible',
        'wrs.weekday',
      )
      .innerJoin(
        'events.weekly_recurring_schedule as wrs',
        're.id',
        'wrs.recurring_event_id',
      );
    if (scheduleId != null) {
      query = query.where('re.id', scheduleId);
    }
    let res = await query;
    return res;
  }

  async getMonthlyRecurringSchedules(
    byWeek: boolean,
    scheduleId: number | undefined,
  ) {
    let query = db('events.recurring_event as re')
      .select(
        're.id',
        're.title',
        're.url',
        're.description',
        're.price',
        're.geocode_id',
        're.organizationId',
        're.authorId',
        're.startTime',
        're.endTime',
        're.requiresPhysicalActivities',
        're.handicapAccessible',
        'mrs.weekNumber',
        'mrs.dayOfMonth',
        'mrs.weekday',
      )
      .innerJoin(
        'events.monthly_recurring_schedule as mrs',
        're.id',
        'mrs.recurring_event_id',
      )
      .whereNotNull(byWeek ? 'weekday' : 'day_of_month');
    if (scheduleId != null) {
      query = query.andWhere('re.id', scheduleId);
    }
    let res = await query;
    return res;
  }

  private queryEvents(
    selectFunc: any,
    query: GetEventsRequest,
    geocode: GetGeocodeResponse,
  ) {
    const res = selectFunc
      .innerJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
      .innerJoin('events.organization as org', 'event.organizationId', 'org.id')
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
