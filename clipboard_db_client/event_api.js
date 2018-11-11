const feathers = require('@feathersjs/feathers');
const express = require('@feathersjs/express');
const errors = require('@feathersjs/errors');
const MongoClient = require('mongodb').MongoClient;
const service = require('feathers-mongodb');

const port = 5000;

MongoClient.connect('mongodb://192.168.99.100:27017/clipboard', {useNewUrlParser: true}).then(client => {
  setup(client);
});

function configureApp() {
    const app = express(feathers());

    // Turn on JSON body parsing for REST services
    app.use(express.json())
    // Turn on URL-encoded body parsing for REST services
    app.use(express.urlencoded({ extended: true }));
    // Set up REST transport using Express
    app.configure(express.rest());

    // Set up an error handler that gives us nicer errors
    app.use(express.errorHandler());

    return app;
}

function setup(client) {
    const app = configureApp();

    app.use('/events', service({
        Model: client.db('clipboard').collection('event'),
        paginate: {
            default: 25,
            max: 100
        }
    }));

    app.service('events').hooks(eventHooks);

    const server = app.listen(port);

    server.on('listening', () => 
        console.log(`Event service started at http://localhost:${port}`));
}

const eventHooks = {
    before: {
        async find(context) {
            let query = context.params.query;
            
            // Yo dawg, we heard you like json so we put json in your query language so you can query with json while you query for json
            var search_fields = [
                { name: 'start_timestamp', func: '$gte', val: parseInt(query.start_timestamp) },
                { name: 'end_timestamp', func: '$lte', val: parseInt(query.end_timestamp) },
                { name:'organization', func: '$eq', val: query.organization }
            ]
            
            let filters = search_fields
            .filter(param => param.val !== NaN && param.val !== undefined && param.val !== null)
            .map(param => ({
                [param.name]: {
                    [param.func]: param.val
                }
            }));

            let and_clause = {'$and': filters};

            for (val of search_fields) {
                delete query[val.name];
            }
            
            Object.assign(context.params.query, and_clause);
            return context;
        }
    }
}