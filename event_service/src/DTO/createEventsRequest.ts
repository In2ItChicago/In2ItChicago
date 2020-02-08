import { ApiProperty } from '@nestjs/swagger';
import { EventTime } from '@src/DTO/eventTime';
import { IsNotEmpty, IsNumber, IsBoolean, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { CreateEventRequest } from './createEventRequest';

/**
 * Model representing a request for creating an event
 */
export class CreateEventsRequest {
    
    @ValidateNested({ each: true })
    @Type(() => CreateEventRequest)
    @ApiProperty({isArray: true, type: CreateEventRequest})
    public events: CreateEventRequest[];
}
