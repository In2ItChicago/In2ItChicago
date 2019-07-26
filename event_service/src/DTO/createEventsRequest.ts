import { ApiModelProperty } from '@nestjs/swagger';
import { EventTime } from './eventTime';

export class CreateEventsRequest {
    @ApiModelProperty()
    organization: string;
    @ApiModelProperty()
    eventTime: EventTime;
    @ApiModelProperty()
    title: string;
    @ApiModelProperty()
    address: string;
    @ApiModelProperty()
    url: string;
    @ApiModelProperty()
    description: string;
    @ApiModelProperty()
    price: number;
}
