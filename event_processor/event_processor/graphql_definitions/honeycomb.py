from gql import gql
definition = gql('''
            query EVENTS($search: EventSearchInput) {
                events(search: $search) {
                    docs {
                        id
                        name
                        date
                        startTime
                        endTime
                        shortDescription
                        description
                        favorite
                        open
                        category {
                            id
                            name
                        }
                        program {
                            id
                            shortDescription
                            description
                            addressLineOne
                            addressLineTwo
                            city
                            state
                            postal
                        }
                    }
                }
            }
        ''')