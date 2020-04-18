export enum UserMetadata {
    // Can do anything
    GodUser = 'godUser',
    // Can create/update/view users
    UserAdmin = 'userAdmin',
    // Can perform system maintenance tasks like cleaning up data
    SystemAdmin = 'systemAdmin',
    // Can create events for one or more organizations
    EventCreator = 'eventCreator',
    // Can create events for any organization (used for scraping)
    EventAdmin = 'eventAdmin',
    // List of orgs associated with an event creator
    AllowedOrgs = 'allowedOrgs'
}