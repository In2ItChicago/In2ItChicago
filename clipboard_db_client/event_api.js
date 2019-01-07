const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const errors = require('@feathersjs/errors');
const MongoClient = require('mongodb').MongoClient;
const service = require('feathers-mongodb');
const swagger = require('feathers-swagger');
const _ = require('lodash');
const axios = require('axios');

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
const sleep = require('util').promisify(setTimeout)
let lastExecuted = new Date();

(async () => {
    let client = new MongoClient('mongodb://clipboard_db:27017/clipboard', {
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
        }))

    let eventModel = client.db('clipboard').collection('event');
    let geocodeModel = client.db('clipboard').collection('geocode');
    eventModel.ensureIndex({'start_timestamp': 1, 'end_timestamp': 1, 'organization': 1}, function(errorMsg, indexName) {
        if (!indexName) {
            throw errors.GeneralError(errorMsg);
        }
    });

    geocodeModel.ensureIndex({ 'expireAt': 1 }, { expireAfterSeconds: 0 }, function(errorMsg, indexName) {
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
            default: 25,
            max: 100
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

function transformResult(mongoResult) {
    start_timestamp = mongoResult.event_time.start_timestamp;
    end_timestamp = mongoResult.event_time.end_timestamp;
    id = mongoResult._id.toString();

    delete mongoResult.event_time;
    delete mongoResult._id;
    
    Object.assign(mongoResult, {
        start_time: timeFromTimestamp(start_timestamp),
        start_date: dateFromTimestamp(start_timestamp),
        end_time: timeFromTimestamp(end_timestamp),
        end_date: dateFromTimestamp(end_timestamp),
        id: id
    })
    
    return mongoResult;
}

async function getGeocode(address) {
    let base_url = 'https://nominatim.openstreetmap.org/search';
    let diff = new Date() - lastExecuted;
    if (diff <= geocodeApiDelayMilliseconds) {
        await sleep(diff);
    }
    let response = await axios.get(`${base_url}?q=${address}&format=json`);
    lastExecuted = new Date();
    let data = response.data[0];
    let result = {
        'address': address,
        'lat': data.lat, 
        'lon': data.lon
    };
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

const eventHooks = {
    before: {
        async find(context) {
            let query = context.params.query;
            
            var search_fields = {
                'start_timestamp': { func: '$gte', val: parseInt(query.start_timestamp) },
                'end_timestamp': { func: '$lte', val: parseInt(query.end_timestamp) }
            }

            function mapParams(param) {
                let field = search_fields[param]
                let ret = field ? { [field.func]: field.val }: { ['$eq']: query[param] }
                return {
                    [param]: ret
                }; 
            }
            let keys = _.keys(query)

            let newParams = _.pickBy(query, (value, key) => key.startsWith('$'))

            let mongoFilters = keys
            .filter(key => !key.startsWith('$'))
            .map(mapParams);
            
            if (mongoFilters.length > 0) {
                let and_clause = {'$and': mongoFilters};
                Object.assign(newParams, and_clause);
            }
            context.params.query = newParams;
            return context;
        },

        async create(context) {
            let invalid = context.data.filter(data => !(data.organization && data.event_time.start_timestamp && data.event_time.end_timestamp));
            if (invalid.length > 0) {
                throw new errors.BadRequest('Invalid events. organization, start_timestamp, and end_timestamp are required', invalid);
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
    }
}

const geocodeHooks = {
    before: {
        async find(context) {
            let query = context.params.query;
            context.params.query = { 'address': {'$eq': query.address }};
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
                return context;
            }
            let address = context.params.address;
            let result = await getGeocode(address);
            context.result = [result];
            await this.create(result);
            return context;
        }
    }
}