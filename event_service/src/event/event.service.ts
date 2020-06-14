import { Injectable, HttpService, Inject, HttpStatus } from '@nestjs/common';
import { EventDAL } from '@src/DAL/eventDAL';
import { timestampToDate } from '@src/utilities';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { CreateEventsRequest } from '@src/DTO/createEventsRequest';
import * as _ from 'lodash';
import { GeocodeService } from '@src/geocode/geocode.service';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { plainToClass } from 'class-transformer';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { CreateEventRequest } from '@src/DTO/createEventRequest';
import { HttpException } from '@nestjs/common/exceptions/http.exception'
import { Schedule } from './rschedule';
import * as moment from 'moment';
import { RRule, RRuleSet, rrulestr } from 'rrule'
import { CreateRecurringEventRequest } from '@src/DTO/createRecurringEventRequest';

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

    async createRecurringEvent(eventRequest: CreateRecurringEventRequest) {
        let mapping = new Map([
            ['Monday', RRule.MO], 
            ['Tuesday', RRule.TU], 
            ['Wednesday', RRule.WE],
            ['Thursday', RRule.TH],
            ['Friday', RRule.FR],
            ['Saturday', RRule.SA],
            ['Sunday', RRule.SU]
        ]);

        let today = new Date();
        let end = new Date();
        end.setMonth(end.getMonth() + 3);
        
        if (eventRequest.isWeekly) {
            let rule = new RRule({
                freq: RRule.WEEKLY,
                interval: 1,
                byweekday: eventRequest.weeklyRecurringDays.map(d => mapping.get(d)),
                dtstart: today,
                until: end
            });
            console.log(rule.all());
        }
        else if (eventRequest.isByWeekday){
            const rule = new RRule({
                freq: RRule.MONTHLY,
                interval: 1,
                bysetpos: eventRequest.monthlyRecurringWeekNumber,
                byweekday: [mapping.get(eventRequest.monthlyRecurringWeekday)],
                dtstart: today,
                until: end
            });
            console.log(rule.all());
        }
        else {
            const rule = new RRule({
                freq: RRule.MONTHLY,
                interval: 1,
                bymonthday: eventRequest.monthlyRecurringDay,
                dtstart: today,
                until: end
            });
            console.log(rule.all());
        }
    }

    async createEvents(contextData: CreateEventRequest[]) {
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

        await this.eventDAL.createEvents(contextData);
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
