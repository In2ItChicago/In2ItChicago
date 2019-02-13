const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const errors = require('@feathersjs/errors');
const MongoClient = require('mongodb').MongoClient;
const service = require('feathers-mongodb');
const swagger = require('feathers-swagger');

const docs = require('./docs.js');
const event = require('./event.js');
const geocode = require('./geocode.js');
const settings = require('./settings.js');

(async () => { 
    let client = new MongoClient(`mongodb://mongo:${settings.mongoPort}`, {
        useNewUrlParser: true,
    });
    let currentTries = 0;
    async function connect() {
        try {
            await client.connect();
            console.log('DB connection succeeded');
            setup(client);
        }
        catch (error) { 
            if (error.name === 'MongoNetworkError' && currentTries < settings.retries) {
                currentTries++;
                console.log('DB connection attempt: ' + currentTries);
                connect();
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

    app.use('/neighborhoods', {
        async find(params) {
            return geocodeModel.distinct('neighborhood');
        }, docs: docs.neighborhoodDocs
    });

    let geoService = Object.assign(service({
        Model: geocodeModel,
        whitelist: settings.additionalMongoFilters
    }), {
        docs: docs.geocodeDocs
    });

    let eventService = Object.assign(service({
        Model: eventModel,
        paginate: {
            default: 25
        },
        multi: true,
        whitelist: settings.additionalMongoFilters
    }), {
        docs: docs.eventDocs
    });

    app.use('/geocode', geoService);
    app.service('geocode').hooks(geocode.geocodeHooks);

    app.use('/events', eventService);
    app.service('events').hooks(event.eventHooks);    

    const server = app.listen(settings.port);

    server.on('listening', () => 
        console.log(`Event service started at http://localhost:${settings.port}`));

    // Set up an error handler that gives us nicer errors
    // This only works at the bottom of the setup logic for some reason
    app.use(express.errorHandler());
}