module.exports = {
    eventDocs: {
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
    },
    geocodeDocs: {
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
    },
    neighborhoodDocs: {
        description: 'Return all available neighborhoods',
        definitions: {
            'neighborhood list': {
                $ref: '#/definitions/neighborhood'
            },
            neighborhood: {
                'type': 'object'
            }
        },
        find: {
            parameters: []
        }
    },
    radiusDocs: {
        description: 'Return all events in a certain radius',
        definitions: {
            'radius list': {
                $ref: '#/definitions/radius'
            },
            radius: {
                'type': 'object'
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
                    description: 'Miles',
                    in: 'query',
                    name: 'miles',
                    type: 'float'
                }
            ]
        }
    }
}