module.exports = {
    port: 5000,
    // OpenStreetMaps only allows 1 query per second
     geocodeApiDelayMilliseconds: 1000,
    // Expire geo data after a set amount of time to prevent the database from getting too big
    // Use a random expiration time between min and max to avoid too much data expiring at the same time
    minExpireAfterDays: 15,
    maxExpireAfterDays: 30,
    retries: 20,
    // feathers only whitelists certain filters by default, need to add these manually or it will throw an error
    additionalMongoFilters: ['$eq', '$and'],
    mongoPort: 27017
}
