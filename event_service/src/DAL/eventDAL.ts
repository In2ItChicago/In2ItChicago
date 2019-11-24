import * as knex from 'knex';
import * as knexStringcase from 'knex-stringcase';
import * as _ from 'lodash';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';

const DEFAULT_LIMIT = 25;
const MILES_TO_METERS = 1609.34;
const makeVector = `to_tsvector(organization || ' ' || title || ' ' || description)`;
const db = knex(knexStringcase({
    client: 'postgresql',
    connection: {
        host: process.env.HOST,
        user: 'postgres',
        password: 'postgres',
        database: 'events'
    }
}));

/**
 * Middleware for processing a raw event object to event response objects? 
 */
export class EventDAL {
    async getEvents(query: GetEventsRequest, geocode: GetGeocodeResponse): Promise<any> {

        let result = await this.queryEvents(db('events.event as event').select(
            'event.id',
            'event.title',
            'event.url',
            'event.description',
            'event.organization',
            'event.price',
            'event.startTime',
            'event.endTime',
            'event.category',
            'event.createdDate',
            'geo.address',
            'geo.lat',
            'geo.lon',
            'geo.neighborhood')
            .select(db.raw(`${query.keywords ? `ts_rank_cd(${makeVector}, to_tsquery(?))` : '?'} as rank`, query.keywords ? query.keywords : 0)), query, geocode)
        .offset(query.offset || 0)
        .limit(query.limit || DEFAULT_LIMIT)
        .orderBy('rank', 'desc')
        .orderBy('event.isManual', 'desc')
        .orderBy('event.startTime', 'asc');

        const resultCount = await this.queryEvents(db('events.event as event').count('*'), query, geocode).first();
                    
        return {'totalCount': resultCount.count, 'events': result};
    }

    async createEvents(data: any): Promise<any> {
        const val = await db('events.event').insert(data);
        return val;
    }

    async deleteEvents(organizations: string[]): Promise<any> {
        const val = await db('events.event').whereIn('organization', organizations).del();
        return val;
    }

    async nullifyGeocodeIds() {
        await db('events.event').update('geocodeId', null);
    }

    async deleteAllEvents() {
        await db('events.event').del();
    }

    private queryEvents(selectFunc: any, query: GetEventsRequest, geocode: GetGeocodeResponse) {
        const res = selectFunc
                    .innerJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
                    .where('event.startTime', '>=', query.startTime || '01-01-1970')
                    .andWhere('event.endTime', '<=', query.endTime || '12-31-2099')
                    .modify((queryBuilder) => {
                        if (geocode) {
                            queryBuilder
                                .whereNotNull('geo.lat')
                                .whereNotNull('geo.lon')
                                .andWhere('geo.lat', '!=', 'NaN')
                                .andWhere('geo.lon', '!=', 'NaN')
                                .andWhereRaw('earth_distance(ll_to_earth(geo.lat, geo.lon), ll_to_earth(?, ?)) <= ?', [geocode.lat, geocode.lon, query.miles * MILES_TO_METERS])
                        }
                        
                        if (query.neighborhood) {
                            queryBuilder.andWhere('geo.neighborhood', '=', query.neighborhood);
                        }
                        if (query.keywords) {
                            queryBuilder.andWhereRaw(`${makeVector} @@ to_tsquery(?)`, query.keywords)
                        }
                    });
        return res;
    }
}
