import { Controller, Get, Query, Post, Body, Res, HttpStatus, Bind } from '@nestjs/common';
import { EventService } from './event.service';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { CreateEventsRequest } from '@src/DTO/createEventsRequest';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { ApiUseTags, ApiImplicitBody, ApiResponse } from '@nestjs/swagger';

@ApiUseTags('events')
@Controller('events')
export class EventController {
    constructor(private readonly eventService: EventService) {}

    @Get()
    @ApiResponse({status: 200, type: GetEventsResponse, isArray: true, description: 'Event list'})
    async getEvents(@Query() request: GetEventsRequest): Promise<GetEventsResponse[]> {
        const response = await this.eventService.getEvents(request);
        return response;
    }

    // There seeems to be a bug that requires the ApiImplicitBody name to be 'Array'
    @Post()
    @ApiImplicitBody({name: 'Array', type: CreateEventsRequest, isArray: true})
    @ApiResponse({status: 201, description: 'Created'})
    async createEvents(@Body() request: CreateEventsRequest[]) {
        await this.eventService.createEvents(request);
    }
}
