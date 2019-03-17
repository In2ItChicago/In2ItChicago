import { MongoClient, Collection } from 'mongodb';
import { GeneralError } from '@feathersjs/errors';
import * as service from 'feathers-mongodb';
import * as _ from 'lodash';
import * as settings from './settings';
import * as docs from './docs';
import * as common from './common';
import { Params } from '@feathersjs/feathers';

class Mongo {
    geocodeModel: Collection<any>
    eventModel: Collection<any>

    initCollections(client: MongoClient) {
        this.eventModel = client.db('in2it').collection('event');
        this.geocodeModel = client.db('in2it').collection('geocode');
        this.eventModel.createIndex({'event_time.start_timestamp': 1, 'event_time.end_timestamp': 1, 'organization': 1, 'geocode.lat': 1, 'geocode.lon': 1}, function(errorMsg, indexName) {
            if (!indexName) {
                throw new GeneralError(errorMsg);
            }
        });

        this.geocodeModel.createIndex({ 'expireAt': 1 }, { expireAfterSeconds: 0 }, function(errorMsg, indexName) {
            if (!indexName) {
                throw new GeneralError(errorMsg);
            }
        });

        this.geocodeModel.createIndex({ 'address': 1, 'neighborhood': 1 }, function(errorMsg, indexName) {
            if (!indexName) {
                throw new GeneralError(errorMsg);
            }
        });
    }

    async initialize(): Promise<void> {
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
                return;
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
        let self = this;
        return {
            async find(params: Params) {
                return self.geocodeModel.distinct('neighborhood', {});
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
    let id = mongoResult._id.toString();

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