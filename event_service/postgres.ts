import * as knex from 'knex'
import { Params, Query } from '@feathersjs/feathers';
import * as _ from 'lodash';
import { sql, DatabaseConnectionType, createPool, PrimitiveValueExpressionType } from 'slonik';

import { neighborhoodDocs, eventDocs, geocodeDocs } from './docs';
import { sleep, timeFromTimestamp, dateFromTimestamp } from './common';

const pool = createPool('postgres://postgres:postgres@postgres:5432/events');

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
                let result = await db.select('*').from('geocode.location');
                //let result = await pool.query(sql`select * from geocode.location`);
                return result;
            }, docs: neighborhoodDocs
        }
    }

    get eventService() {
        return {
            async find(params: Params) {
                let query = params.query;
                if (!query) {
                    return null;
                }
                
                let result = await db({geo: 'geocode.location', event: 'events.event'}).select('*')
                    .from('events.event as event')
                    .leftOuterJoin('geocode.location as geo', 'event.geocode_id', 'geo.id')
                    .where('event.start_timestamp', '>=', query.start_timestamp.val || 0)
                    .andWhere('event.end_timestamp', '<=', query.end_timestamp.val || 99999999999999999999)
                  
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
