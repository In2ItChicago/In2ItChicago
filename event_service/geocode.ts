import { Application, HookContext, HooksObject } from "@feathersjs/feathers";

const _ = require('lodash');
const axios = require('axios');
const fs = require('fs');
const GeoJsonGeometriesLookup = require('geojson-geometries-lookup');

const common = require('./common.ts');
const settings = require('./settings');
const mongo = require('./mongo.ts');

const geojsonData = fs.readFileSync('chicago_neighborhoods.geojson');
const geojsonContent = JSON.parse(geojsonData);
const geoLookup = new GeoJsonGeometriesLookup(geojsonContent);

class AddressResult {
    address: string
    lat: number
    lon: number
    neighborhood: string
}

let lastExecuted = new Date();

async function getGeocode(address: string): Promise<AddressResult> {
    let baseUrl = 'https://nominatim.openstreetmap.org/search';
    let diff = new Date().valueOf() - lastExecuted.valueOf();
    if (diff <= settings.geocodeApiDelayMilliseconds) {
        await common.sleep(diff);
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
                // searching by address and neighborhood causes issues if the neighborhood doesn't match the address
                if (query.address && query.neighborhood) {
                    delete query.neighborhood;
                }
                context.params.query = mongo.buildQuery(query);
            
                // This is only here so it's easier to access
                context.params.address = query.address;
                return context;
            },
    
            async create(context: HookContext) {
                context.data.expireAt = common.randomExpirationTime();
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
                let result = null;
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
        error: common.errorHandler
    }
}
