import { ApiModelProperty } from '@nestjs/swagger';
import { EventTime } from './eventTime';
import { IsNotEmpty, IsNumber } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateEventsRequest {
    @IsNotEmpty()
    @ApiModelProperty()
    organization: string;

    @IsNotEmpty()
    @ApiModelProperty()
    @Type(() => EventTime)
    eventTime: EventTime;

    @IsNotEmpty()
    @ApiModelProperty()
    title: string;

    @IsNotEmpty()
    @ApiModelProperty()
    address: string;

    @IsNotEmpty()
    @ApiModelProperty()
    url: string;

    @IsNotEmpty()
    @ApiModelProperty()
    description: string;
    
    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty()
    price: number;
}
