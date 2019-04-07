import * as knex from 'knex'
import { Params, Query } from '@feathersjs/feathers';
import * as _ from 'lodash';

import { neighborhoodDocs, eventDocs, geocodeDocs } from './docs';
import { sleep, timeFromTimestamp, dateFromTimestamp } from './common';

const db = knex({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events'
  });

// function clause(statement: string, variable: PrimitiveValueExpressionType[] | undefined) {
//     return sql.raw(variable == null ? '' : statement, variable);
// }

export class Postgres {
    get neighborhoodService() {
        let self = this;
        return {
            async find(params: Params) {
                let result = await db('geocode.location')
                    .distinct('neighborhood')
                    .whereNotNull('neighborhood');
                    
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
                debugger;
                let result = await db().select('*')
                    .from('events.event as event')
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
                    });
                
                return result;
            },
            async create(data: any, params: Params) {
                data.forEach(element => {
                    delete element.address;
                });
                
                let val = await db('events.event').insert(data).then(() => console.log('data inserted'));
                return null;
            },
            async remove(id, params: Params) {
                let query = params.query;
                if (query) {
                    let val = db('events.event').whereIn('organization', query.organization).del().then(() => console.log('data deleted'));
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
                    result = await db.select('*').from('geocode.location');
                    return result;
                }
                result = await db.select('*').from('geocode.location').where(filter, value);
                return result;
            },
            async create(data: any, params: Params) {
                let val = await db('geocode.location').returning('id').insert(data);
                return val;
            },
            docs: geocodeDocs
        }
    }
}

export function buildQuery(query: Query, searchFields={}, join='$and'): _.Dictionary<any> {
    return Object.assign(query, searchFields);
}

export function transformResult(result: any): object {
    let startTimestamp = result.event_time.start_timestamp;
    let endTimestamp = result.event_time.end_timestamp;
    //let id = result._id.toString();

    delete result.event_time;
    delete result._id;
    
    Object.assign(result, {
        start_time: timeFromTimestamp(startTimestamp),
        start_date: dateFromTimestamp(startTimestamp),
        end_time: timeFromTimestamp(endTimestamp),
        end_date: dateFromTimestamp(endTimestamp),
        start_timestamp: startTimestamp,
        end_timestamp: endTimestamp,
    })
    
    return result;
}
