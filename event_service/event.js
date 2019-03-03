const _ = require('lodash');
const GeoPoint = require('geopoint');
const errors = require('@feathersjs/errors');
const common = require('./common.js');

async function geoSearch(app, address, miles) {
    searchBounds = {};
    let foundAddress = await app.service('geocode').find({'query': {'address': `${address} US`}});
    if (foundAddress.lat && foundAddress.lon) {
        let point = new GeoPoint(parseFloat(foundAddress.lat), parseFloat(foundAddress.lon));
        let bounds = point.boundingCoordinates(miles);
        searchBounds = {
            'min_lat': Math.min(bounds[0]._degLat, bounds[1]._degLat),
            'max_lat': Math.max(bounds[0]._degLat, bounds[1]._degLat),
            'min_lon': Math.min(bounds[0]._degLon, bounds[1]._degLon),
            'max_lon': Math.max(bounds[0]._degLon, bounds[1]._degLon),
        };
    }

    return searchBounds;
}


module.exports = {
    eventHooks: function(app) {
        return {
            before: {
                async find(context) {
                    let query = context.params.query;
                    
                    if ((query.address && !query.miles) || (query.miles && !query.address)) {
                        throw new errors.BadRequest("address and miles must be used together");
                    }

                    let searchBounds = {};
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
                        'min_lat': { name: 'geocode.lat', func: '$gte', val: searchBounds.min_lat },
                        'min_lon': { name: 'geocode.lon', func: '$gte', val: searchBounds.min_lon },
                        'max_lat': { name: 'geocode.lat', func: '$lte', val: searchBounds.max_lat },
                        'max_lon': { name: 'geocode.lon', func: '$lte', val: searchBounds.max_lon }
                    }
        
                    context.params.query = common.mongoSearch(query, searchFields);
                    return context;
                },
        
                async create(context) {
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
                async find(context) {
                    context.result.data = context.result.data.map(mongoResult => common.transformResult(mongoResult));
                    return context;
                }
            },
            error: common.errorHandler
        }
    }
}
