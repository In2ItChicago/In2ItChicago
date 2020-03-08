import { Controller, Get, Query, Post, Body, Res, HttpStatus, Bind, Delete } from '@nestjs/common';
import { EventService } from '@src/event/event.service';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { CreateEventsRequest } from '@src/DTO/createEventsRequest';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { ApiTags, ApiBody, ApiResponse, ApiBearerAuth, ApiBasicAuth } from '@nestjs/swagger';
import { Roles } from '@src/decorators/roles.decorator';

/**
 * An interface class to get, create, or clear events. 
 */
@ApiBearerAuth()
@ApiTags('events')
@Controller('events')
export class EventController {
    constructor(private readonly eventService: EventService) {}

    @Get()
    @Roles('isAdmin')
    @ApiResponse({status: 200, type: GetEventsResponse, isArray: true, description: 'Event list'})
    async getEvents(@Query() request: GetEventsRequest): Promise<GetEventsResponse> {
        return await this.eventService.getEvents(request);
    }

    @Post()
    @ApiResponse({status: 201, description: 'Created'})
    async createEvents(@Body() request: CreateEventsRequest) {
        await this.eventService.createEvents(request.events);
    }

    @Delete('ClearAllEvents')
    @ApiResponse({status: 200, description: 'Deleted'})
    async clearAllEvents() {
        await this.eventService.clearAllEvents();
    }

    @Delete('CleanupEvents')
    @ApiResponse({status: 200, description: 'Deleted'})
    async cleanupEvents() {
        await this.eventService.cleanupEvents();
    }
}
