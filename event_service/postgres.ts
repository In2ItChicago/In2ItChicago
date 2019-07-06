import * as knex from 'knex'
import { Params, Query } from '@feathersjs/feathers';
import * as _ from 'lodash';

import { neighborhoodDocs, eventDocs, geocodeDocs } from './docs';
import { sleep, timeFromTimestamp, dateFromTimestamp } from './common';

const db = knex({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events'
});

const DEFAULT_LIMIT = 25;

export class Postgres {
    get neighborhoodService() {
        let self = this;
        return {
            async find(params: Params) {
                let result = await db('geocode.location')
                    .distinct('neighborhood')
                    .whereNotNull('neighborhood')
                    .orderBy('neighborhood');
                    
                return result;
            }, docs: neighborhoodDocs
        }
    }

    get eventService() {
        return {
            async find(params: Params) {
                if (!params.query) {
                    return null;
                }
                let query = params.query;

                let result = await db('events.event as event').select('*')
                    .leftOuterJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
                    .where('event.start_time', '>=', query.start_timestamp || '01-01-1970')
                    .andWhere('event.end_time', '<=', query.end_timestamp || '12-31-2099')
                    .modify(function(queryBuilder) {
                        if (query.searchBounds) {
                            let searchBounds = query.searchBounds;
                            queryBuilder
                                .andWhere('geo.lat', '>=', searchBounds.minLat)
                                .andWhere('geo.lat', '<=', searchBounds.maxLat)
                                .andWhere('geo.lon', '>=', searchBounds.minLon)
                                .andWhere('geo.lon', '<=', searchBounds.maxLon)
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
                debugger;
                return result;
            },
            async create(data: any, params: Params) {
                let val = await db('events.event').insert(data);
                return null;
            },
            async remove(id, params: Params) {
                let query = params.query;
                if (query) {
                    let val = await db('events.event').whereIn('organization', query.organization).del();
                }
                return null;
            },
            docs: eventDocs
        }
    }

    get geoService() {
        return {
            async find(params: Params) {
                let filter = '';
                let value = '';
                let result: knex.QueryBuilder;
                if (params.address) {
                    filter = 'address';
                    value = params.address;
                }
                else if (params.neighborhood){
                    filter = 'neighborhood';
                    value = params.neighborhood;
                }
                else {
                    let allGeo = await db.select('*').from('geocode.location');
                    return allGeo;
                }
                let filteredGeo = await db.select('*').from('geocode.location').where(filter, value);
                return filteredGeo;
            },
            async create(data: any, params: Params) {
                let val = await db('geocode.location').returning('id').insert(data);
                return val;
            },
            docs: geocodeDocs
        }
    }
}