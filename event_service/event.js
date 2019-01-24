const _ = require('lodash');
const common = require('./common.js');

module.exports = {
    eventHooks: {
        before: {
            async find(context) {
                let query = context.params.query;
                
                var searchFields = {
                    'start_timestamp': { name: 'event_time.start_timestamp', func: '$gte', val: parseInt(query.start_timestamp) },
                    'end_timestamp': { name: 'event_time.end_timestamp', func: '$lte', val: parseInt(query.end_timestamp) }
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
