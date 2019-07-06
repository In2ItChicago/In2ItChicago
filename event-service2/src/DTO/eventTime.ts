import { ApiModelProperty } from '@nestjs/swagger';

export class EventTime {
    @ApiModelProperty()
    startTimestamp: number;
    @ApiModelProperty()
    endTimestamp: number;
}
