const MongoClient = require('mongodb').MongoClient;
const service = require('feathers-mongodb');
const _ = require('lodash');
const settings = require('./settings.js');
const docs = require('./docs.js');
const common = require('./common.js');
deasync = require('deasync');

class Mongo {
    constructor() {
        this.geocodeModel = null;
        this.eventModel = null;
    }

    initCollections(client) {
        this.eventModel = client.db('in2it').collection('event');
        this.geocodeModel = client.db('in2it').collection('geocode');
        this.eventModel.createIndex({'event_time.start_timestamp': 1, 'event_time.end_timestamp': 1, 'organization': 1, 'geocode.lat': 1, 'geocode.lon': 1}, function(errorMsg, indexName) {
            if (!indexName) {
                throw errors.GeneralError(errorMsg);
            }
        });

        this.geocodeModel.createIndex({ 'expireAt': 1 }, { expireAfterSeconds: 0 }, function(errorMsg, indexName) {
            if (!indexName) {
                throw errors.GeneralError(errorMsg);
            }
        });

        this.geocodeModel.createIndex({ 'address': 1, 'neighborhood': 1 }, function(errorMsg, indexName) {
            if (!indexName) {
                throw errors.GeneralError(errorMsg);
            }
        });
    }

    async initialize() {
        let client = new MongoClient(`mongodb://mongo:${settings.mongoPort}`, {
            useNewUrlParser: true,
        });
        let currentTries = 0;
        let self = this;
        async function connect() {
            try {
                await client.connect();
                console.log('DB connection succeeded');
                self.initCollections(client);
                return client;
            }
            catch (error) { 
                if (error.name === 'MongoNetworkError') {
                    currentTries++;
                    console.log('DB connection attempt: ' + currentTries);
                    common.sleep(settings.sleepTime);
                    await connect();
                }
                else {
                    console.log(error);
                }
            }
        }
        await connect();
    }
    

    get neighborhoodService() {
        return {
            async find(params) {
                return this.geocodeModel.distinct('neighborhood');
            }, docs: docs.neighborhoodDocs
        }
    }

    get eventService() {
        return Object.assign(service({
                Model: this.eventModel,
                paginate: {
                    default: 25
                },
                multi: true,
                whitelist: settings.additionalMongoFilters
            }), {
                docs: docs.eventDocs
            });
    }

    get geoService() {
        return Object.assign(service({
            Model: this.geocodeModel,
            whitelist: settings.additionalMongoFilters
        }), {
            docs: docs.geocodeDocs
        });
    }
}

function buildQuery(query, searchFields={}, join='$and') {
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
        start_time: common.timeFromTimestamp(startTimestamp),
        start_date: common.dateFromTimestamp(startTimestamp),
        end_time: common.timeFromTimestamp(endTimestamp),
        end_date: common.dateFromTimestamp(endTimestamp),
        start_timestamp: startTimestamp,
        end_timestamp: endTimestamp,
        id: id
    })
    
    return mongoResult;
}

module.exports = {
    Mongo: Mongo,
    transformResult: transformResult,
    buildQuery: buildQuery
}