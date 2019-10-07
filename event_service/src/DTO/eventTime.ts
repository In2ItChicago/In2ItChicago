import { ApiModelProperty } from '@nestjs/swagger';
import { IsNumber } from 'class-validator';
import { Type } from 'class-transformer';

/**
 * Model representing an EventTime
 * Note: Why is this not being used in the other response or request models??
 */
export class EventTime {
    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty()
    startTimestamp: number;
    
    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty()
    endTimestamp: number;
}
