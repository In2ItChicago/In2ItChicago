import { Application, HookContext, HooksObject } from "@feathersjs/feathers";
import * as _ from 'lodash';
import axios from 'axios';
import { readFileSync } from 'fs';
import * as GeoJsonGeometriesLookup from 'geojson-geometries-lookup';

import { sleep, errorHandler, randomExpirationTime } from './common';
import { geocodeApiDelayMilliseconds } from './settings';
import { buildQuery } from './mongo';
import { GeneralError } from "@feathersjs/errors";

const geojsonData = readFileSync('chicago_neighborhoods.geojson');
const geojsonContent = JSON.parse(geojsonData.toString());
const geoLookup = new GeoJsonGeometriesLookup(geojsonContent);

class AddressResult {
    address: string
    lat: number
    lon: number
    neighborhood: string | null
}

let lastExecuted = new Date();

async function getGeocode(address: string): Promise<AddressResult | null> {
    let baseUrl = 'https://nominatim.openstreetmap.org/search';
    let diff = new Date().valueOf() - lastExecuted.valueOf();
    if (diff <= geocodeApiDelayMilliseconds) {
        await sleep(diff);
    }
    let response = await axios.get(`${baseUrl}?q=${address}&format=json`);
    lastExecuted = new Date();

    if (response.data.length === 0) {
        return null;
    }

    let data = response.data[0];
    let result: AddressResult = {
        address,
        lat: parseFloat(data.lat), 
        lon: parseFloat(data.lon),
        neighborhood: null
    };

    let geojsonPoint = { type: "Point", coordinates: [data.lon, data.lat] }; 
    let matches = geoLookup.getContainers(geojsonPoint).features;
    if (matches.length > 0) {
        result.neighborhood = matches[0].properties.pri_neigh;
    }
    return result;
}

export function geocodeHooks(app: Application<any>): Partial<HooksObject> {
    return {
        before: {
            async find(context: HookContext): Promise<HookContext> {
                let query = context.params.query; 
                if (!query) {
                    throw new GeneralError('Query not supplied');
                }
                // searching by address and neighborhood causes issues if the neighborhood doesn't match the address
                if (query.address && query.neighborhood) {
                    delete query.neighborhood;
                }
                context.params.query = buildQuery(query);
            
                // This is only here so it's easier to access
                context.params.address = query.address;
                return context;
            },
    
            async create(context: HookContext) {
                context.data.expireAt = randomExpirationTime();
                return context;
            }
        },
        after: {
            async find(context: HookContext): Promise<HookContext> {
                // Geocode already found in database. No need to query web service.
                if (context.result.length > 0) {
                    if (context.params.address) {
                        context.result = context.result[0];
                    }
                    return context;
                }
                let result: AddressResult | null = null;
                if (context.params.address) {
                    result = await getGeocode(context.params.address);
                }
                
                if (result == null) {
                    return context;
                }
                context.result = result;
                await this.create(result);
                return context;
            }
        },
        error: {
            all(ctx) {
                return errorHandler(ctx);
            }
        }
    }
}
