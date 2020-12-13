import {
  Controller,
  Get,
  Query,
  Post,
  Body,
  Delete,
  UseGuards,
} from '@nestjs/common';
import { EventService } from '@src/event/event.service';
import { GetEventsRequest } from '@src/DTO/getEventsRequest';
import { GetEventsResponse } from '@src/DTO/getEventsResponse';
import { ApiTags, ApiBody, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { Roles } from '@src/decorators/roles.decorator';
import { OrganizationsGuard } from '@src/guards/organizations.guard';
import { UserMetadata } from '@src/enums/userMetadata';
import { CreateRecurringEventRequest } from '@src/DTO/createRecurringEventRequest';
import { CreateEventRequest } from '@src/DTO/createEventRequest';

/**
 * An interface class to get, create, or clear events.
 */
@ApiBearerAuth()
@ApiTags('events')
@Controller('events')
export class EventController {
  constructor(private readonly eventService: EventService) {}

  @Get()
  @ApiResponse({
    status: 200,
    type: GetEventsResponse,
    isArray: true,
    description: 'Event list',
  })
  async getEvents(
    @Query() request: GetEventsRequest,
  ): Promise<GetEventsResponse> {
    return await this.eventService.getEvents(request);
  }

  @Post()
  @UseGuards(OrganizationsGuard)
  @Roles(UserMetadata.EventCreator, UserMetadata.EventAdmin)
  @ApiResponse({ status: 201, description: 'Created' })
  async createEvents(@Body() request: CreateEventRequest) {
    await this.eventService.createEvents(request);
  }

  @Post('recurringEvent')
  @UseGuards(OrganizationsGuard)
  @Roles(UserMetadata.EventCreator, UserMetadata.EventAdmin)
  @ApiResponse({ status: 201, description: 'Created' })
  async createRecurringEvent(@Body() request: CreateRecurringEventRequest) {
    await this.eventService.createRecurringEvent(request);
  }

  @Roles(UserMetadata.SystemAdmin)
  @Delete('clearAllEvents')
  @ApiResponse({ status: 200, description: 'Deleted' })
  async clearAllEvents() {
    await this.eventService.clearAllEvents();
  }

  @Roles(UserMetadata.SystemAdmin)
  @Delete('cleanupEvents')
  @ApiResponse({ status: 200, description: 'Deleted' })
  async cleanupEvents() {
    await this.eventService.cleanupEvents();
  }
}
