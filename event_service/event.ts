import { Application, HookContext, HooksObject } from '@feathersjs/feathers';
import * as _ from 'lodash';
import * as GeoPoint from 'geopoint';
import { BadRequest, GeneralError } from '@feathersjs/errors';

import { buildQuery, transformResult } from './postgres';
import { errorHandler, timestampToDate, dateFromTimestamp } from './common';

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
                if (!context.params.query) {
                    throw new GeneralError('Query not found');
                }

                let query = context.params.query;
                if ((query.address && !query.miles) || (query.miles && !query.address)) {
                    throw new BadRequest("address and miles must be used together");
                }

                let searchBounds: SearchBounds | null = null;
                if (query.address) {
                    searchBounds = await geoSearch(app, query.address, parseFloat(query.miles));
                    delete query.address;
                    delete query.miles;
                    Object.assign(query, searchBounds);
                }
                    
                //context.params.query = Object.assign(query, searchFields);
                context.params.query.searchBounds = searchBounds;
                return context;
            },
    
            async create(context: HookContext): Promise<HookContext> {
                let invalid = context.data.filter(data => !(
                    data.organization && 
                    data.event_time && 
                    (data.event_time.start_timestamp || data.event_time.start_timestamp === 0) && 
                    (data.event_time.end_timestamp || data.event_time.end_timestamp === 0)));
                if (invalid.length > 0) {
                    throw new BadRequest('Invalid events. organization, event_time.start_timestamp, and event_time.end_timestamp are required', invalid);
                }

                for (let i = 0; i < context.data.length; i++) {
                    Object.assign(context.data[i], {
                        start_time: timestampToDate(context.data[i].event_time.start_timestamp),
                        end_time: timestampToDate(context.data[i].event_time.end_timestamp)
                    });
                    delete context.data[i].event_time;
                }
                
                let organizations = _(context.data)
                    .groupBy(d => d.organization)
                    .map((value, key) => key)
                    .value();
                
                
                await this.remove(null, {
                    'query': {
                        'organization': organizations
                    }
                });
                return context;
            }
        },
        after: {
            async find(context: HookContext): Promise<HookContext> {
                if (context.result.data) {
                    context.result.data = context.result.data.map(result => transformResult(result));
                }
                
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
