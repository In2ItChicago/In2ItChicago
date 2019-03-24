import { Application, HookContext, HooksObject } from '@feathersjs/feathers';
import * as _ from 'lodash';
import * as GeoPoint from 'geopoint';
import { BadRequest, GeneralError } from '@feathersjs/errors';

import { buildQuery, transformResult } from './mongo';
import { errorHandler } from './common';

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
                if (!query) {
                    throw new GeneralError('Query not found');
                }
                
                if ((query.address && !query.miles) || (query.miles && !query.address)) {
                    throw new BadRequest("address and miles must be used together");
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
                    'minLat': { name: 'geocode.lat', func: '$gte', val: searchBounds.minLat },
                    'minLon': { name: 'geocode.lon', func: '$gte', val: searchBounds.minLon },
                    'maxLat': { name: 'geocode.lat', func: '$lte', val: searchBounds.maxLat },
                    'maxLon': { name: 'geocode.lon', func: '$lte', val: searchBounds.maxLon }
                }
    
                context.params.query = buildQuery(query, searchFields);
                return context;
            },
    
            async create(context: HookContext): Promise<HookContext> {
                let invalid = context.data.filter(data => !(data.organization && data.event_time && data.event_time.start_timestamp && data.event_time.end_timestamp));
                if (invalid.length > 0) {
                    throw new BadRequest('Invalid events. organization, event_time.start_timestamp, and event_time.end_timestamp are required', invalid);
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
                context.result.data = context.result.data.map(mongoResult => transformResult(mongoResult));
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
