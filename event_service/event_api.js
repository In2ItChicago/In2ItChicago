const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const cors = require('cors');
const errors = require('@feathersjs/errors');
const MongoClient = require('mongodb').MongoClient;
const service = require('feathers-mongodb');
const swagger = require('feathers-swagger');

const docs = require('./docs.js');
const event = require('./event.js');
const geocode = require('./geocode.js');
const settings = require('./settings.js');
const common = require('./common.js');
const Mongo = require('./mongo.js').Mongo;

function setup() {
    let client = new Mongo();
    client.initialize().then(() => {
        const app = express(feathers());

        // Turn on JSON body parsing for REST services
        app
        .use(express.json({limit: '50mb'}))
        // Turn on URL-encoded body parsing for REST services
        .use(express.urlencoded({ extended: true }))
        // Enable Cross-origin resource sharing
        .use(cors())
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

        app.use('/status', {
            async find(params) {
                return 'available'
            }
        });

        app.use('/neighborhoods', client.neighborhoodService);

        app.use('/geocode', client.geoService);
        app.service('geocode').hooks(geocode.geocodeHooks(app));

        app.use('/events', client.eventService);
        app.service('events').hooks(event.eventHooks(app));    

        const server = app.listen(settings.port);

        server.on('listening', () => 
            console.log(`Event service started at http://localhost:${settings.port}`));

        // Set up an error handler that gives us nicer errors
        // This only works at the bottom of the setup logic for some reason
        app.use(express.errorHandler());
    });
}
    

setup();