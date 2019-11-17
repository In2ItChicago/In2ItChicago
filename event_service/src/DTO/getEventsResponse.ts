import { ApiModelProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { EventResponse } from '@src/DTO/eventResponse';

/**
 * Model for the response returned from an events query??
 */
export class GetEventsResponse {
    @Type(() => Number)
    @ApiModelProperty()
    totalCount: number;

    @Type(() => EventResponse)
    @ApiModelProperty()
    events: EventResponse[];
}
