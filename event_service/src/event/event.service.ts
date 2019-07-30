import { Injectable, HttpService, Inject } from '@nestjs/common';
import { SearchBounds } from 'src/interfaces/searchBounds';
import { EventDAL } from '@src/DAL/eventDAL';
import { timestampToDate } from '../utilities';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { CreateEventsRequest } from '@src/DTO/createEventsRequest';
import * as _ from 'lodash';
import { GeocodeService } from '@src/geocode/geocode.service';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { plainToClass } from 'class-transformer';

@Injectable()
export class EventService {

    constructor(private readonly geocodeService: GeocodeService, @Inject('EventDAL') private readonly eventDAL: EventDAL) {
    }

    async getEvents(query: GetEventsRequest): Promise<GetEventsResponse[]> {
        let searchBounds: SearchBounds | null = null;
        if (query.address) {
            searchBounds = await this.geocodeService.radiusSearch({ address: query.address }, query.miles);
        }

        const events = await this.eventDAL.getEvents(query, searchBounds);

        if (events) {
            const mappedEvents = events.map(result => {
                return plainToClass(GetEventsResponse, Object.assign(result, {
                    startDate: result['startTime'].toLocaleDateString(),
                    startTime: result['startTime'].toLocaleTimeString(),
                    endDate: result['endTime'].toLocaleDateString(),
                    endTime: result['endTime'].toLocaleTimeString()
                }));
            });

            return mappedEvents;
        }
        return [];
    }

    async createEvents(contextData: CreateEventsRequest[]) {
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
}
