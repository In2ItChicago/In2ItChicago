import { ApiModelProperty } from '@nestjs/swagger';
import { EventTime } from '@src/DTO/eventTime';
import { IsNotEmpty, IsNumber, IsBoolean } from 'class-validator';
import { Type } from 'class-transformer';

/**
 * Model representing a request for creating an event
 */
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

    @IsBoolean()
    @Type(() => Boolean)
    @ApiModelProperty()
    isManual: boolean;

    @IsNumber()
    @IsNotEmpty()
    @ApiModelProperty()
    geocodeId: number;
}
