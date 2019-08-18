import { ApiModelProperty } from '@nestjs/swagger';
import { IsNumber } from 'class-validator';
import { Type } from 'class-transformer';

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
