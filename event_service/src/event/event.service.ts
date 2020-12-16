import { Injectable, HttpService, Inject, HttpStatus } from '@nestjs/common';
import { EventDAL } from '@src/DAL/eventDAL';
import { timestampToDate } from '@src/utilities';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import * as _ from 'lodash';
import { GeocodeService } from '@src/geocode/geocode.service';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { plainToClass } from 'class-transformer';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { CreateEventRequest } from '@src/DTO/createEventRequest';
import { HttpException } from '@nestjs/common/exceptions/http.exception';
import { Schedule } from './rschedule';
import * as moment from 'moment';
import { RRule, RRuleSet, rrulestr, Weekday } from 'rrule';
import { CreateRecurringEventRequest } from '@src/DTO/createRecurringEventRequest';

@Injectable()
export class EventService {
  constructor(
    private readonly geocodeService: GeocodeService,
    @Inject('EventDAL') private readonly eventDAL: EventDAL,
  ) {}

  readonly rruleWeekdays: Map<string, Weekday> = new Map([
    ['Monday', RRule.MO],
    ['Tuesday', RRule.TU],
    ['Wednesday', RRule.WE],
    ['Thursday', RRule.TH],
    ['Friday', RRule.FR],
    ['Saturday', RRule.SA],
    ['Sunday', RRule.SU],
  ]);

  async getEvents(query: GetEventsRequest): Promise<GetEventsResponse> {
    let geocode: GetGeocodeResponse | null = null;
    if (query.address) {
      geocode = await this.geocodeService.getGeocode({
        address: query.address,
        lat: null,
        lon: null,
      });
    }
    if (query.keywords) {
      query.keywords = query.keywords.split(' ').join('&');
    }
    const eventResponse = await this.eventDAL.getEvents(query, geocode);

    if (eventResponse.events) {
      eventResponse.events = eventResponse.events.map((result) =>
        Object.assign(result, {
          startDate: result['startTime'].toLocaleDateString(),
          startTime: result['startTime'].toLocaleTimeString(),
          endDate: result['endTime'].toLocaleDateString(),
          endTime: result['endTime'].toLocaleTimeString(),
        }),
      );
      const mappedEvents = plainToClass(GetEventsResponse, eventResponse);
      return mappedEvents;
    }
    return new GetEventsResponse();
  }

  async createRecurringEvent(eventRequest: CreateRecurringEventRequest) {
    let geocode = await this.geocodeService.getGeocode({
      address: eventRequest.address,
      lat: null,
      lon: null,
    });
    let orgId = await this.eventDAL.getOrgId(eventRequest.organization);

    let recurringEventId = await this.eventDAL.createRecurringEvent(
      eventRequest,
      orgId,
      geocode.id,
    );

    if (eventRequest.mode === 'week') {
      await this.eventDAL.createWeeklyRecurringSchedules(
        recurringEventId,
        eventRequest.weeklyRecurringDays,
      );
    } else if (eventRequest.mode === 'weekOfMonth') {
      await this.eventDAL.createMonthlyRecurringEvent(
        recurringEventId,
        eventRequest.monthlyRecurringWeekday,
        eventRequest.monthlyRecurringWeekNumber,
        null,
      );
    } else {
      await this.eventDAL.createMonthlyRecurringEvent(
        recurringEventId,
        null,
        null,
        eventRequest.monthlyRecurringDay,
      );
    }

    await this.generateSchedules(recurringEventId);
  }

  async generateSchedules(scheduleId?: number) {
    let monthlyRecurringSchedulesByWeekday = await this.eventDAL.getMonthlyRecurringSchedules(
      true,
      scheduleId,
    );
    let monthlyRecurringSchedulesByDayOfMonth = await this.eventDAL.getMonthlyRecurringSchedules(
      false,
      scheduleId,
    );
    let weeklyRecurringSchedules = await this.eventDAL.getWeeklyRecurringSchedules(
      scheduleId,
    );

    let allMonthlySchedulesByWeek = this.generateAllSchedules(
      monthlyRecurringSchedulesByWeekday,
      (s) =>
        this.generateMonthlySchedulesByWeek(
          s.startTime,
          s.weekNumber,
          s.weekday,
        ),
    );

    let allMonthlySchedulesByDay = this.generateAllSchedules(
      monthlyRecurringSchedulesByDayOfMonth,
      (s) => this.getMonthlySchedulesByDayOfMonth(s.startTime, s.dayOfMonth),
    );

    let allWeeklySchedules = this.generateAllSchedules(
      weeklyRecurringSchedules,
      (s) => this.getWeeklySchedules(s.startTime, s.weekday),
    );

    let allSchedules = [
      allMonthlySchedulesByWeek,
      allMonthlySchedulesByDay,
      allWeeklySchedules,
    ].flat();

    await this.eventDAL.createEvents(allSchedules);
  }

  private generateAllSchedules(
    schedules: any,
    scheduleFunc: (s: any) => RRule,
  ) {
    return schedules
      .map((s) => ({ dates: scheduleFunc(s).all(), data: s }))
      .map((d) => this.fillSchedules(d.data, d.dates))
      .flat();
  }

  private fillSchedules(data: any, dates: Date[]) {
    return dates.map((d) => ({
      ...data,
      startTime: d,
      endTime: new Date(d.getTime() + (data.endTime - data.startTime)),
    }));
  }

  private getScheduleTimeframe(start: Date) {
    let end = new Date();
    end.setMonth(end.getMonth() + 3);
    return { start, end };
  }

  private generateMonthlySchedulesByWeek(
    startDate: Date,
    monthlyRecurringWeekNumber: number,
    monthlyRecurringWeekday: string,
  ) {
    let { start, end } = this.getScheduleTimeframe(startDate);
    const rule = new RRule({
      freq: RRule.MONTHLY,
      interval: 1,
      bysetpos: monthlyRecurringWeekNumber,
      byweekday: [this.rruleWeekdays.get(monthlyRecurringWeekday)],
      dtstart: start,
      until: end,
    });

    return rule;
  }

  private getMonthlySchedulesByDayOfMonth(
    startDate: Date,
    monthlyRecurringDay: number,
  ) {
    const { start, end } = this.getScheduleTimeframe(startDate);
    const rule = new RRule({
      freq: RRule.MONTHLY,
      interval: 1,
      bymonthday: monthlyRecurringDay,
      dtstart: start,
      until: end,
    });

    return rule;
  }

  private getWeeklySchedules(startDate: Date, weeklyRecurringDay: string) {
    const { start, end } = this.getScheduleTimeframe(startDate);
    let rule = new RRule({
      freq: RRule.WEEKLY,
      interval: 1,
      byweekday: this.rruleWeekdays.get(weeklyRecurringDay),
      dtstart: start,
      until: end,
    });

    return rule;
  }

  private generateSchedules2(eventRequest: CreateRecurringEventRequest) {
    let mapping = new Map([
      ['Monday', RRule.MO],
      ['Tuesday', RRule.TU],
      ['Wednesday', RRule.WE],
      ['Thursday', RRule.TH],
      ['Friday', RRule.FR],
      ['Saturday', RRule.SA],
      ['Sunday', RRule.SU],
    ]);

    let today = new Date();
    let end = new Date();
    end.setMonth(end.getMonth() + 3);

    if (eventRequest.mode === 'week') {
      let rule = new RRule({
        freq: RRule.WEEKLY,
        interval: 1,
        byweekday: eventRequest.weeklyRecurringDays.map((d) => mapping.get(d)),
        dtstart: today,
        until: end,
      });
      console.log(rule.all());
    } else if (eventRequest.mode === 'weekOfMonth') {
      const rule = new RRule({
        freq: RRule.MONTHLY,
        interval: 1,
        bysetpos: eventRequest.monthlyRecurringWeekNumber,
        byweekday: [mapping.get(eventRequest.monthlyRecurringWeekday)],
        dtstart: today,
        until: end,
      });
      console.log(rule.all());
    } else {
      const rule = new RRule({
        freq: RRule.MONTHLY,
        interval: 1,
        bymonthday: eventRequest.monthlyRecurringDay,
        dtstart: today,
        until: end,
      });
      console.log(rule.all());
    }
  }

  async createEvent(contextData: CreateEventRequest) {
    let geocode = await this.geocodeService.getGeocode({
      address: contextData.address,
      lat: null,
      lon: null,
    });

    let orgId = await this.eventDAL.getOrgId(contextData.organization);

    await this.eventDAL.createEvent(contextData, orgId, geocode.id);
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
