import { ApiModelProperty } from '@nestjs/swagger';

export class GetEventsRequest {
    @ApiModelProperty({type: 'string', format: 'date-time', required: false})
    startTime: Date;
    @ApiModelProperty({type: 'string', format: 'date-time',  required: false})
    endTime: Date;
    @ApiModelProperty({required: false})
    organization: string;
    @ApiModelProperty({required: false})
    address: string;
    @ApiModelProperty({required: false})
    miles: number;
    @ApiModelProperty({required: false})
    neighborhood: string;
    @ApiModelProperty({required: false})
    limit: number;
    @ApiModelProperty({required: false})
    offset: number;
}
