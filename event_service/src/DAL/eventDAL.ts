import * as knex from 'knex';
import * as knexStringcase from 'knex-stringcase';
import * as _ from 'lodash';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { SearchBounds } from '@src/interfaces/searchBounds';
import { Get } from '@nestjs/common';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { AnyTxtRecord } from 'dns';

const DEFAULT_LIMIT = 25;
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
    async getEvents(query: GetEventsRequest, searchBounds: SearchBounds): Promise<any> {
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
            'geo.neighborhood'), query, searchBounds)
        .offset(query.offset || 0)
        .limit(query.limit || DEFAULT_LIMIT)
        .orderBy('event.isManual', 'desc')
        .orderBy('event.startTime', 'asc');
        debugger;
        if (query.keywords) {
            const searchResults = await this.textSeach(query.keywords);
            const searchIds = searchResults.map(r => r.id);
            result = result.filter(r => searchIds.indexOf(r.id) > -1).map(r => Object.assign(r, searchResults.filter(s => s.id === r.id)[0].score));
        }

        const resultCount = await this.queryEvents(db('events.event as event').count('*'), query, searchBounds)
                    
        return {'totalCount': resultCount[0].count, 'events': result};
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

    async textSeach(keywords: string): Promise<any[]> {
        const res = await db.select(knex.raw(
            `id, ts_rank_cd(vector, query) AS score FROM events.event, to_tsquery(':keywords:') query, to_tsvector(organization || ' ' || title || ' ' || description) vector WHERE vector @@ query order by score desc`, { keywords }
        ));
        return res;
    }

    private queryEvents(selectFunc: any, query: GetEventsRequest, searchBounds: SearchBounds) {
        const res = selectFunc
                    .innerJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
                    .where('event.startTime', '>=', query.startTime || '01-01-1970')
                    .andWhere('event.endTime', '<=', query.endTime || '12-31-2099')
                    .modify((queryBuilder) => {
                        if (searchBounds) {
                            queryBuilder
                                .andWhere('geo.lat', '>=', searchBounds.minLat)
                                .andWhere('geo.lat', '<=', searchBounds.maxLat)
                                .andWhere('geo.lon', '>=', searchBounds.minLon)
                                .andWhere('geo.lon', '<=', searchBounds.maxLon);
                        }
                        if (query.organization) {
                            queryBuilder.andWhere('event.organization', '=', query.organization);
                        }
                        if (query.neighborhood) {
                            queryBuilder.andWhere('geo.neighborhood', '=', query.neighborhood);
                        }
                    });
        return res;
    }
}
