import { ApiModelProperty } from '@nestjs/swagger';

export class GetEventsRequest {
    @ApiModelProperty({type: 'string', format: 'date-time'})
    startTime: Date;
    @ApiModelProperty({type: 'string', format: 'date-time'})
    endTime: Date;
    @ApiModelProperty()
    organization: string;
    @ApiModelProperty()
    address: string;
    @ApiModelProperty()
    miles: number;
    @ApiModelProperty()
    neighborhood: string;
    @ApiModelProperty()
    limit: number;
    @ApiModelProperty()
    offset: number;
}
