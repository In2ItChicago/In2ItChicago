import * as knex from 'knex';
import * as _ from 'lodash';

const DEFAULT_LIMIT = 25;

const db = knex({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events',
});

export class EventDAL {
    async getNeighborhoods(): Promise<Array<Pick<any, 'neighborhood'>>> {
        const result = await db('geocode.location')
                    .distinct('neighborhood')
                    .whereNotNull('neighborhood')
                    .orderBy('neighborhood');

        return result;
    }

    async getEvents(query: any): Promise<any> {
        const result = await db('events.event as event').select('*')
                    .leftOuterJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
                    .where('event.start_time', '>=', query.start_timestamp || '01-01-1970')
                    .andWhere('event.end_time', '<=', query.end_timestamp || '12-31-2099')
                    .modify((queryBuilder) => {
                        if (query.searchBounds) {
                            const searchBounds = query.searchBounds;
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

    async deleteEvents(params: any): Promise<number> {
        const query = params.query;
        if (query) {
            const val = await db('events.event').whereIn('organization', query.organization).del();
            return val;
        }
        return null;
    }

    
}
