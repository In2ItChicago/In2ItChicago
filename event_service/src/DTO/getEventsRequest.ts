import { ApiModelProperty } from '@nestjs/swagger';
import { IsDate, IsEmpty, IsNumber, ValidateIf, IsNotEmpty, IsPositive, IsDefined } from 'class-validator';
import { Type } from 'class-transformer';

export class GetEventsRequest {
    @IsDate()
    @Type(() => Date)
    @ApiModelProperty({type: 'string', format: 'date-time', required: false})
    startTime?: Date;

    @IsDate()
    @Type(() => Date)
    @ApiModelProperty({type: 'string', format: 'date-time',  required: false})
    endTime?: Date;

    @ApiModelProperty({required: false})
    organization?: string;

    @ValidateIf(o => o.miles != null)
    @IsDefined()
    @IsNotEmpty()
    @ApiModelProperty({required: false})
    address?: string;

    @ValidateIf(o => o.address)
    @IsDefined()
    @IsPositive()
    @Type(() => Number)
    @ApiModelProperty({required: false})
    miles?: number;

    @ApiModelProperty({required: false})
    neighborhood?: string;

    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty({required: false})
    limit?: number;

    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty({required: false})
    offset?: number;
}
