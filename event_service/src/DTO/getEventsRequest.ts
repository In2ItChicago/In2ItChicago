import { ApiProperty } from '@nestjs/swagger';
import { IsDate, IsEmpty, IsNumber, ValidateIf, IsNotEmpty, IsPositive, IsDefined, IsOptional } from 'class-validator';
import { Type } from 'class-transformer';

/**
 * Model representing a request for getting a collection of events
 */
export class GetEventsRequest {
    /**
     * The start time to search for the events. Optional.
     */
    @IsOptional()
    @IsDate()
    @Type(() => Date)
    @ApiProperty({type: 'string', format: 'date-time', required: false})
    startTime?: Date;

    /**
     * The end time to search for events? Optional.
     */
    @IsOptional()
    @IsDate()
    @Type(() => Date)
    @ApiProperty({type: 'string', format: 'date-time',  required: false})
    endTime?: Date;

    /**
     * The address of where to search for the events from??? Optional unless "miles" is provided
     */
    @ValidateIf(o => o.miles != null)
    @IsDefined()
    @IsNotEmpty()
    @ApiProperty({required: false})
    address?: string;

    /**
     * How many miles away from the given address to search for events. Optional unless "address" is provided
     */
    @ValidateIf(o => o.address)
    @IsDefined()
    @IsPositive()
    @Type(() => Number)
    @ApiProperty({required: false})
    miles?: number;

    /**
     * The neighborhood where this event is occurring. Optional
     * Note: Should this be an Enum of some kind?? Does typescript have those? 
     */
    @IsOptional()
    @ApiProperty({required: false})
    neighborhood?: string;

    /**
     * Limit the number of events returned by this request??? Optional.
     */
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @ApiProperty({required: false})
    limit?: number;

    /**
     * The offset of events to return by this request. For pagination??? Optional???
     * Note: Should all pagination related variables be required? 
     */
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @ApiProperty({required: false})
    offset?: number;

    /**
     * Keywords for full text search on organization, title, and description
     */
    @IsOptional()
    @ApiProperty({required: false})
    keywords?: string;
}
