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
                let result = db.select('*').from('geocode.Location');
                return result;
            }, docs: neighborhoodDocs
        }
    }

    get eventService() {
        return {
            async find(params: Params) {
                let result = db.select('*').from('events.event');
                return result;
            },
            async create(data: any, params: Params) {
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
                let result = db.select('*').from('geocode.location');
                return result;
            },
            async create(data: any, params: Params) {
                let val = db('geocode.location').insert(data).then(() => console.log('data inserted'));
                return null;
            },
        }
    }
}
