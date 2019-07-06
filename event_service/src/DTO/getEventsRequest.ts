import { ApiModelProperty } from '@nestjs/swagger';

export class GetEventsRequest {
    @ApiModelProperty()
    startTime: Date;
    @ApiModelProperty()
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
