import { Application, HookContext, HooksObject } from "@feathersjs/feathers";

import * as _ from 'lodash';
const mongo = require('./mongo.ts');
const GeoPoint = require('geopoint');
const errors = require('@feathersjs/errors');
const common = require('./common.ts');

class SearchBounds {
    minLat: number
    maxLat: number
    minLon: number
    maxLon: number
}

async function geoSearch(app: Application<any>, address: string, miles: number): Promise<SearchBounds> {
    let searchBounds = new SearchBounds();
    let foundAddress = await app.service('geocode').find({'query': {'address': `${address} US`}});
    if (foundAddress.lat && foundAddress.lon) {
        let point = new GeoPoint(parseFloat(foundAddress.lat), parseFloat(foundAddress.lon));
        let bounds = point.boundingCoordinates(miles);
        searchBounds = {
            minLat: Math.min(bounds[0]._degLat, bounds[1]._degLat),
            maxLat: Math.max(bounds[0]._degLat, bounds[1]._degLat),
            minLon: Math.min(bounds[0]._degLon, bounds[1]._degLon),
            maxLon: Math.max(bounds[0]._degLon, bounds[1]._degLon),
        };
    }

    return searchBounds;
}

export function eventHooks(app: Application<any>): Partial<HooksObject> {
    return {
        before: {
            async find(context: HookContext): Promise<HookContext> {
                let query = context.params.query;
                
                if ((query.address && !query.miles) || (query.miles && !query.address)) {
                    throw new errors.BadRequest("address and miles must be used together");
                }

                let searchBounds = new SearchBounds();
                if (query.address) {
                    searchBounds = await geoSearch(app, query.address, parseFloat(query.miles));
                    delete query.address;
                    delete query.miles;
                    Object.assign(query, searchBounds);
                }
                    
                var searchFields = {
                    'start_timestamp': { name: 'event_time.start_timestamp', func: '$gte', val: parseInt(query.start_timestamp) },
                    'end_timestamp': { name: 'event_time.end_timestamp', func: '$lte', val: parseInt(query.end_timestamp) },
                    'neighborhood': { name: 'geocode.neighborhood', func: '$eq', val: query.neighborhood },
                    'min_lat': { name: 'geocode.lat', func: '$gte', val: searchBounds.minLat },
                    'min_lon': { name: 'geocode.lon', func: '$gte', val: searchBounds.minLon },
                    'max_lat': { name: 'geocode.lat', func: '$lte', val: searchBounds.maxLat },
                    'max_lon': { name: 'geocode.lon', func: '$lte', val: searchBounds.maxLon }
                }
    
                context.params.query = mongo.buildQuery(query, searchFields);
                return context;
            },
    
            async create(context: HookContext): Promise<HookContext> {
                let invalid = context.data.filter(data => !(data.organization && data.event_time && data.event_time.start_timestamp && data.event_time.end_timestamp));
                if (invalid.length > 0) {
                    throw new errors.BadRequest('Invalid events. organization, event_time.start_timestamp, and event_time.end_timestamp are required', invalid);
                }
                let organizations = _(context.data)
                    .groupBy(d => d.organization)
                    .map((value, key) => key)
                    .value();
                
                
                await this.remove(null, {
                    'query': {
                        'organization': {
                            '$in': organizations
                        }
                    }
                });
                return context;
            }
        },
        after: {
            async find(context: HookContext): Promise<HookContext> {
                context.result.data = context.result.data.map(mongoResult => mongo.transformResult(mongoResult));
                return context;
            }
        },
        error: common.errorHandler
    }
}
