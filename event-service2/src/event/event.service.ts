import { Injectable } from '@nestjs/common';
import { SearchBounds } from 'src/interfaces/searchBounds';
import { EventDAL } from 'src/DAL/eventDAL';
import { timestampToDate } from 'src/utilities';
import { GetEventsRequest } from 'src/DTO/getEventsRequest';
import { CreateEventsRequest } from 'src/DTO/createEventsRequest';
import * as _ from 'lodash';
import { GeocodeService } from 'src/geocode/geocode.service';
import { GetEventsResponse } from 'src/DTO/getEventsResponse';

@Injectable()
export class EventService {
    private readonly eventDAL: EventDAL;

    constructor(private readonly geocodeService: GeocodeService) {
        this.eventDAL = new EventDAL();
    }

    async getEvents(query: GetEventsRequest): Promise<GetEventsResponse[]> {
        // if (!context.params.query) {
        //     throw new GeneralError('Query not found');
        // }
        
        // if ((query.address && !query.miles) || (query.miles && !query.address)) {
        //     throw new BadRequest("address and miles must be used together");
        // }

        let searchBounds: SearchBounds | null = null;
        if (query.address) {
            searchBounds = await this.geocodeService.radiusSearch(query.address, query.miles);
            delete query.address;
            delete query.miles;
        }
        //context.params.query = Object.assign(query, searchFields);
        //context.params.query.searchBounds = searchBounds;

        const events = this.eventDAL.getEvents(query, searchBounds);

        // if (events) {
        //     const mappedEvents = events.map(result => {
        //         Object.assign(result, {
        //             start_date: result.start_time.toLocaleDateString(),
        //             start_time: result.start_time.toLocaleTimeString(),
        //             end_date: result.end_time.toLocaleDateString(),
        //             end_time: result.end_time.toLocaleTimeString()
        //         });
                
        //         return mappedEvents;
        //     });
        // }
        return events;
    }

    async createEvents(contextData: CreateEventsRequest[]) {
        const invalid = contextData.filter(data => !(
            data.organization && 
            data.eventTime && 
            (data.eventTime.startTimestamp || data.eventTime.startTimestamp === 0) &&
            (data.eventTime.endTimestamp || data.eventTime.endTimestamp === 0)));
        // if (invalid.length > 0) {
        //     throw new BadRequest('Invalid events. organization, event_time.start_timestamp, and event_time.end_timestamp are required', invalid);
        // }

        for (let i = 0; i < contextData.length; i++) {
            Object.assign(contextData[i], {
                start_time: timestampToDate(contextData[i].eventTime.startTimestamp),
                end_time: timestampToDate(contextData[i].eventTime.endTimestamp)
            });
            delete contextData[i].eventTime;
            delete contextData[i].address;
        }

        const organizations = _(contextData)
            .groupBy(d => d.organization)
            .map((value, key) => key)
            .value();

        if (organizations) {
            await this.eventDAL.deleteEvents(organizations);
        }

        this.eventDAL.createEvents(contextData);
    }
}
