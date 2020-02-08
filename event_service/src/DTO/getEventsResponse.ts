import { ApiProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { EventResponse } from '@src/DTO/eventResponse';

/**
 * Model for the response returned from an events query??
 */
export class GetEventsResponse {
    @Type(() => Number)
    @ApiProperty()
    totalCount: number;

    @Type(() => EventResponse)
    @ApiProperty({isArray: true, type: EventResponse})
    events: EventResponse[];
}
