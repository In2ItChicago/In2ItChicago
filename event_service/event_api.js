const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const errors = require('@feathersjs/errors');
const MongoClient = require('mongodb').MongoClient;
const service = require('feathers-mongodb');
const swagger = require('feathers-swagger');
const _ = require('lodash');
const axios = require('axios');
const fs = require('fs');
const GeoJsonGeometriesLookup = require('geojson-geometries-lookup');

const port = 5000;
const timeout = 1000;
// OpenStreetMaps only allows 1 query per second
const geocodeApiDelayMilliseconds = 1000;
// Expire geo data after a set amount of time to prevent the database from getting too big
// Use a random expiration time between min and max to avoid too much data expiring at the same time
const minExpireAfterDays = 15;
const maxExpireAfterDays = 30;
const retries = 20;
const additionalMongoFilters = ['$eq', '$and'];
const sleep = require('util').promisify(setTimeout);
const geojsonData = fs.readFileSync('chicago_neighborhoods.geojson');
const geojsonContent = JSON.parse(geojsonData);
const geoLookup = new GeoJsonGeometriesLookup(geojsonContent);

let lastExecuted = new Date();

(async () => {
    let client = new MongoClient('mongodb://mongo:27017', {
        useNewUrlParser: true,
    });
    let currentTries = 0;
    async function connect() {
        try {
            await client.connect();
            setup(client);
        }
        catch (error) {
            if (error.name === 'MongoNetworkError' && currentTries < retries) {
                currentTries++;
                console.log('DB connection attempt: ' + currentTries);
                setTimeout(connect, timeout);
            }
            else {
                console.log(error);
            }
        }
    }
    connect();
})();

function setup(client) {
    const app = express(feathers());

    // Turn on JSON body parsing for REST services
    app
        .use(express.json({limit: '50mb'}))
        // Turn on URL-encoded body parsing for REST services
        .use(express.urlencoded({ extended: true }))
        // Set up REST transport using Express
        .configure(express.rest())
        .configure(swagger({
            docsPath: '/docs',
            uiIndex: true,
            info: {
                title: 'Event API',
                description: 'Event API'
              }
        }));

    let eventModel = client.db('in2it').collection('event');
    let geocodeModel = client.db('in2it').collection('geocode');
    eventModel.ensureIndex({'event_time.start_timestamp': 1, 'event_time.end_timestamp': 1, 'organization': 1}, function(errorMsg, indexName) {
        if (!indexName) {
            throw errors.GeneralError(errorMsg);
        }
    });

    geocodeModel.ensureIndex({ 'expireAt': 1 }, { expireAfterSeconds: 0 }, function(errorMsg, indexName) {
        if (!indexName) {
            throw errors.GeneralError(errorMsg);
        }
    });

    geocodeModel.ensureIndex({ 'address': 1, 'neighborhood': 1 }, function(errorMsg, indexName) {
        if (!indexName) {
            throw errors.GeneralError(errorMsg);
        }
    });

    app.use('/status', {
        async find(params) {
            return 'available'
        }
    });

    let geoService = Object.assign(service({
        Model: geocodeModel,
        whitelist: additionalMongoFilters
    }), {
        docs: {
            description: 'Geocoding service',
            definitions: {
                'geocode list': {
                    $ref: '#/definitions/geocode' 
                },
                geocode: {
                    "type": "object"
                }
            },
            find: {
                parameters: [
                    {
                        description: 'Address',
                        in: 'query',
                        name: 'address',
                        type: 'string'
                    },
                    {
                        description: 'Neighborhood',
                        in: 'query',
                        name: 'neighborhood',
                        type: 'string'
                    }
                ]
            }
        }
    });

    app.use('/geocode', geoService);

    app.service('geocode').hooks(geocodeHooks);

    let eventService = Object.assign(service({
        Model: eventModel,
        paginate: {
            default: 25
        },
        multi: true,
        whitelist: additionalMongoFilters
    }), {
        docs: {
            description: 'Event service',
            definitions: {
                'events list': {
                    $ref: '#/definitions/events' 
                },
                event: {
                    type: 'object',
                    required: [ 'organization', 'start_timestamp', 'end_timestamp' ],
                    properties: {
                        organization: {
                            type: "string",
                            description: "organization"
                        },
                        start_timestamp: {
                            type: "integer",
                            "description": "event start time"
                        },
                        end_timestamp: {
                            type: "integer",
                            "description": "event end time"
                        }
                    }
                },
                events: {
                    type: 'array',
                    items: {
                        type: 'object',
                        $ref: '#/definitions/event' 
                    }
                }
            },
            find: {
                parameters: [
                    {
                        description: 'start_timestamp',
                        in: 'query',
                        name: 'start_timestamp',
                        type: 'integer'
                    },
                    {
                        description: 'end_timestamp',
                        in: 'query',
                        name: 'end_timestamp',
                        type: 'integer'
                    },
                    {
                        description: 'organization',
                        in: 'query',
                        name: 'organization',
                        type: 'string'
                    },
                    {
                        description: 'limit',
                        in: 'query',
                        name: '$limit',
                        type: 'string'
                    },
                    {
                        description: 'skip',
                        in: 'query',
                        name: '$skip',
                        type: 'string'
                    },
                ]
            }
        }
    });

    app.use('/events', eventService);

    app.service('events').hooks(eventHooks);

    const server = app.listen(port);

    server.on('listening', () => 
        console.log(`Event service started at http://localhost:${port}`));

    // Set up an error handler that gives us nicer errors
    // This only works at the bottom of the setup logic for some reason
    app.use(express.errorHandler());
}

function timestampToDate(timestamp) {
    return new Date(timestamp * 1000);
}
function dateFromTimestamp(timestamp) {
    return timestampToDate(timestamp).toLocaleDateString();
}

function timeFromTimestamp(timestamp) {
    return timestampToDate(timestamp).toLocaleTimeString();
}

function mongoSearch(query, searchFields={}, join='$and') {
    function mapParams(param) {
        let field = searchFields[param]
        let name = field ? field.name : param
        let ret = field ? { [field.func]: field.val }: { '$eq': query[param] }
        return {
            [name]: ret
        }; 
    }
    let keys = _.keys(query)

    let mongoFilters = keys
    .filter(key => !key.startsWith('$'))
    .map(mapParams);

    let newParams = _.pickBy(query, (value, key) => key.startsWith('$'));

    if (mongoFilters.length > 0) {
        let joinedClause = {[join]: mongoFilters};
        Object.assign(newParams, joinedClause);
    }

    return newParams;
}

function transformResult(mongoResult) {
    let startTimestamp = mongoResult.event_time.start_timestamp;
    let endTimestamp = mongoResult.event_time.end_timestamp;
    id = mongoResult._id.toString();

    delete mongoResult.event_time;
    delete mongoResult._id;
    
    Object.assign(mongoResult, {
        start_time: timeFromTimestamp(startTimestamp),
        start_date: dateFromTimestamp(startTimestamp),
        end_time: timeFromTimestamp(endTimestamp),
        end_date: dateFromTimestamp(endTimestamp),
        start_timestamp: startTimestamp,
        end_timestamp: endTimestamp,
        id: id
    })
    
    return mongoResult;
}

async function getGeocode(address) {
    let baseUrl = 'https://nominatim.openstreetmap.org/search';
    let diff = new Date() - lastExecuted;
    if (diff <= geocodeApiDelayMilliseconds) {
        await sleep(diff);
    }
    let response = await axios.get(`${baseUrl}?q=${address}&format=json`);
    lastExecuted = new Date();

    if (response.data.length === 0) {
        return null;
    }

    let data = response.data[0];
    let result = {
        'address': address,
        'lat': data.lat, 
        'lon': data.lon
    };

    let geojsonPoint = { type: "Point", coordinates: [data.lon, data.lat] }; 
    let matches = geoLookup.getContainers(geojsonPoint).features;
    if (matches.length > 0) {
        result.neighborhood = matches[0].properties.pri_neigh;
    }
    return result;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function daysToMilliseconds(days) {
    return days * 24 * 60 * 60 * 1000;
}

function addDaysToDate(date, days) {
    return new Date(date.getTime() + daysToMilliseconds(days));
}

function randomExpirationTime() {
    let expirationTime = getRandomInt(minExpireAfterDays, maxExpireAfterDays);
    return addDaysToDate(new Date(), expirationTime);
}

const errorHandler = ctx => {
    if (ctx.error) {
        const error = ctx.error;
        if (!error.code) {
            const newError = new errors.GeneralError(`server error: ${error.stack}`);
            ctx.error = newError;
            return ctx;
        }
        
        console.log({
            message: ctx.error.message,
            stack: ctx.error.stack,
            data: ctx.error.data
        });
        return ctx;
    }
};

const eventHooks = {
    before: {
        async find(context) {
            let query = context.params.query;
            
            var searchFields = {
                'start_timestamp': { name: 'event_time.start_timestamp', func: '$gte', val: parseInt(query.start_timestamp) },
                'end_timestamp': { name: 'event_time.end_timestamp', func: '$lte', val: parseInt(query.end_timestamp) }
            }

            context.params.query = mongoSearch(query, searchFields);
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
            context.result.data = context.result.data.map(mongoResult => transformResult(mongoResult));
            return context;
        }
    },
    error: errorHandler
}

const geocodeHooks = {
    before: {
        async find(context) {
            let query = context.params.query; 
            // searching by address and neighborhood causes issues if the neighborhood doesn't match the address
            if (query.address && query.neighborhood) {
                delete query.neighborhood;
            }
            context.params.query = mongoSearch(query);
           
            // This is only here so it's easier to access
            context.params.address = query.address;
            return context;
        },

        async create(context) {
            context.data.expireAt = randomExpirationTime();
            return context;
        }
    },
    after: {
        async find(context) {
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
    error: errorHandler
}