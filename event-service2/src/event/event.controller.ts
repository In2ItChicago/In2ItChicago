import { Controller, Get, Query, Post, Body, Res, HttpStatus } from '@nestjs/common';
import { EventService } from './event.service';
import { GetEventsRequest } from 'src/DTO/getEventsRequest';
import { CreateEventsRequest } from 'src/DTO/createEventsRequest';
import { GetEventsResponse } from 'src/DTO/getEventsResponse';

@Controller('event')
export class EventController {
    constructor(private readonly eventService: EventService) {}

    @Get()
    async getEvents(@Query() request: GetEventsRequest): Promise<GetEventsResponse[]> {
        const response = await this.eventService.getEvents(request);
        return response;
    }

    @Post()
    async createEvents(@Body() request: CreateEventsRequest[]) {
        await this.eventService.createEvents(request);
    }
}
