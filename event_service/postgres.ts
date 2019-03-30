import * as knex from 'knex'
import { Params } from '@feathersjs/feathers';

import { neighborhoodDocs, eventDocs, geocodeDocs } from './docs';
import { create } from 'domain';
import { finished } from 'stream';

const db = knex({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events'
  });

export class Postgres {
    get neighborhoodService() {
        let self = this;
        return {
            async find(params: Params) {
                let result = db.select('*').from('geocode.location');
                return result;
            }, docs: neighborhoodDocs
        }
    }

    get eventService() {
        return {
            async find(params: Params) {
                let result = db.select('*').from('events.event').leftOuterJoin('geocode.location', 'events.event.geocode_id', 'geocode.location.id');
                return result;
            },
            async create(data: any, params: Params) {
                data.forEach(element => {
                    element.geocode_id = element.geocode.id;
                    delete element.address;
                    delete element.geocode;
                });
                let val = db('events.event').insert(data).then(() => console.log('data inserted'));
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
                    return db.select('*').from('geocode.location');
                }
                result = db.select('*').from('geocode.location').where(filter, value);
                return result;
            },
            async create(data: any, params: Params) {
                delete data.expireAt;
                let val = db('geocode.location').insert(data).then(() => console.log('data inserted'));
                return null;
            },
            docs: geocodeDocs
        }
    }
}
