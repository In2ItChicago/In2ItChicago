import * as knex from 'knex';
import * as _ from 'lodash';
import { GetGeocodeRequest } from 'src/DTO/getGeocodeRequest';
import { GetGeocodeResponse } from 'src/DTO/getGeocodeResponse';

const db = knex({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events',
});

export class GeocodeDAL {
    async getGeocode(params: GetGeocodeRequest): Promise<any> {
        let filter = '';
        let value = '';

        if (params.address) {
            filter = 'address';
            value = params.address;
        }
        else if (params.neighborhood) {
            filter = 'neighborhood';
            value = params.neighborhood;
        }
        else {
            const allGeo = await db.select('*').from('geocode.location');
            return allGeo;
        }
        const filteredGeo = await db.select('*').from('geocode.location').where(filter, value);
        return filteredGeo;
    }

    async createGeocode(data: GetGeocodeResponse): Promise<any> {
        const val = await db('geocode.location').returning('id').insert(data);
        return val;
    }
}