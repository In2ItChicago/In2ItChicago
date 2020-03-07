import * as _ from 'lodash';
import { GetGeocodeRequest } from '@src/DTO/getGeocodeRequest';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { CreateGeocodeRequest } from '@src/DTO/createGeocodeRequest';
import { randomExpirationTime } from '@src/utilities';
import { SearchNeighborhoodRequest } from '@src/DTO/searchNeighborhoodRequest';
import { getDb } from '@src/DAL/setup';

// Max number of geocodes not tied to events to cache
const MAX_GEOCODES = 1000;

const db = getDb('events');

/**
 * Middleware for processing geocode requests??? 
 */
export class GeocodeDAL {
    async getNeighborhoods(): Promise<Object[]> {
        const result = await db('geocode.location')
                    .distinct('neighborhood')
                    .whereNotNull('neighborhood')
                    .orderBy('neighborhood');

        return result;
    }

    async getAllGeocodes(): Promise<Object[]> {
        const response = await db.select('id', 'address', 'lat', 'lon', 'neighborhood')
            .from('geocode.location');

        return response;
    }

    async getGeocode(params: GetGeocodeRequest): Promise<Object[]> {
        const result = await db('geocode.location')
            .select('id', 'address', 'lat', 'lon', 'neighborhood')
            .where('address', params.address);

        return result;
    }

    async searchNeighborhood(params: SearchNeighborhoodRequest): Promise<Object[]> {
        const result = await db('geocode.location')
            .select('id', 'address', 'lat', 'lon', 'neighborhood')
            .where('neighborhood', params.neighborhood);

        return result;
    }

    async createGeocode(data: CreateGeocodeRequest): Promise<number> {
        data.expireAt = randomExpirationTime();
        const val = await db('geocode.location').returning('id').insert(data);
        return val[0];
    }

    async deleteAllGeocodes() {
        await db('geocode.location').del();
    }

    async cleanUpGeocodes() {
        await db('geocode.location as geo')
            .whereNotExists(db('events.event as event').select('*').whereRaw('event.geocode_id = geo.id'))
            .orderBy('geo.expireAt', 'asc')
            .offset(MAX_GEOCODES)
            .del();
    }
}
