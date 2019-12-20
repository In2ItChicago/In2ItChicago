import { Injectable, HttpService, Inject } from '@nestjs/common';
import { EventDAL } from '@src/DAL/eventDAL';
import { timestampToDate } from '@src/utilities';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { CreateEventsRequest } from '@src/DTO/createEventsRequest';
import * as _ from 'lodash';
import { GeocodeService } from '@src/geocode/geocode.service';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { plainToClass } from 'class-transformer';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';

@Injectable()
export class EventService {

    constructor(private readonly geocodeService: GeocodeService, @Inject('EventDAL') private readonly eventDAL: EventDAL) {
    }

    async getEvents(query: GetEventsRequest): Promise<GetEventsResponse> {
        let geocode: GetGeocodeResponse | null = null;
        if (query.address) {
            geocode = await this.geocodeService.getGeocode({ address: query.address, lat: null, lon: null });
        }
        if (query.keywords) {
            query.keywords = query.keywords.split(' ').join('&');
        }
        const eventResponse = await this.eventDAL.getEvents(query, geocode);

        if (eventResponse.events) {
            eventResponse.events = eventResponse.events.map(result => Object.assign(result, {
                    startDate: result['startTime'].toLocaleDateString(),
                    startTime: result['startTime'].toLocaleTimeString(),
                    endDate: result['endTime'].toLocaleDateString(),
                    endTime: result['endTime'].toLocaleTimeString()
                }));
            const mappedEvents = plainToClass(GetEventsResponse, eventResponse);
            return mappedEvents;
        }
        return new GetEventsResponse();
    }

    async createEvents(contextData: CreateEventsRequest[]) {
        contextData = contextData.map(c => plainToClass(CreateEventsRequest, c));
        const invalid = contextData.filter(data => !(
            data.organization && 
            data.eventTime && 
            (data.eventTime.startTimestamp || data.eventTime.startTimestamp === 0) &&
            (data.eventTime.endTimestamp || data.eventTime.endTimestamp === 0)));

        for (let i = 0; i < contextData.length; i++) {
            Object.assign(contextData[i], {
                start_time: timestampToDate(contextData[i].eventTime.startTimestamp),
                end_time: timestampToDate(contextData[i].eventTime.endTimestamp),
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

    async clearAllEvents() {
        await this.geocodeService.clearAllGeocodes();
        await this.eventDAL.deleteAllEvents();
    }

    async cleanupEvents() {
        await this.geocodeService.cleanupGeocodes();
        await this.eventDAL.cleanupEvents();
    }
}
