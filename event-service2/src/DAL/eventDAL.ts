import * as knex from 'knex';
import * as knexStringcase from 'knex-stringcase';
import * as _ from 'lodash';
import { GetEventsRequest } from 'src/DTO/getEventsRequest';
import { SearchBounds } from 'src/interfaces/searchBounds';
import { Get } from '@nestjs/common';
import { GetEventsResponse } from 'src/DTO/getEventsResponse';

const DEFAULT_LIMIT = 25;

const db = knex(knexStringcase({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events',
}));

export class EventDAL {
    async getNeighborhoods(): Promise<string[]> {
        const result = await db('geocode.location')
                    .distinct('neighborhood')
                    .whereNotNull('neighborhood')
                    .orderBy('neighborhood');

        return result.map(r => r.neighborhood);
    }

    async getEvents(query: GetEventsRequest, searchBounds: SearchBounds): Promise<GetEventsResponse[]> {
        let result: GetEventsResponse[];
        result = await db('events.event as event').select('*')
                    .leftOuterJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
                    .where('event.start_time', '>=', query.startTime || '01-01-1970')
                    .andWhere('event.end_time', '<=', query.endTime || '12-31-2099')
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
                    })
                    .offset(query.offset || 0)
                    .limit(query.limit || DEFAULT_LIMIT)
                    .orderBy('event.start_time');
        return result;
    }

    async createEvents(data: any): Promise<number[]> {
        const val = await db('events.event').insert(data);
        return val;
    }

    async deleteEvents(organizations: string[]): Promise<number> {
        const val = await db('events.event').whereIn('organization', organizations).del();
        return val;
    }

    
}
