const _ = require('lodash');
const errors = require('@feathersjs/errors');

const settings = require('./settings.js');

module.exports = {
    sleep: (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs)),
    errorHandler(ctx) {
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
    },

    timestampToDate(timestamp) {
        return new Date(timestamp * 1000);
    },

    dateFromTimestamp(timestamp) {
        return this.timestampToDate(timestamp).toLocaleDateString();
    },
    
    timeFromTimestamp(timestamp) {
        return this.timestampToDate(timestamp).toLocaleTimeString();
    },
    
    getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    },
    
    daysToMilliseconds(days) {
        return days * 24 * 60 * 60 * 1000;
    },
    
    addDaysToDate(date, days) {
        return new Date(date.getTime() + this.daysToMilliseconds(days));
    },
    
    randomExpirationTime() {
        let expirationTime = this.getRandomInt(settings.minExpireAfterDays, settings.maxExpireAfterDays);
        return this.addDaysToDate(new Date(), expirationTime);
    },
    
    mongoSearch(query, searchFields={}, join='$and') {
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
    },
    
    transformResult(mongoResult) {
        let startTimestamp = mongoResult.event_time.start_timestamp;
        let endTimestamp = mongoResult.event_time.end_timestamp;
        id = mongoResult._id.toString();
    
        delete mongoResult.event_time;
        delete mongoResult._id;
        
        Object.assign(mongoResult, {
            start_time: this.timeFromTimestamp(startTimestamp),
            start_date: this.dateFromTimestamp(startTimestamp),
            end_time: this.timeFromTimestamp(endTimestamp),
            end_date: this.dateFromTimestamp(endTimestamp),
            start_timestamp: startTimestamp,
            end_timestamp: endTimestamp,
            id: id
        })
        
        return mongoResult;
    }
}
