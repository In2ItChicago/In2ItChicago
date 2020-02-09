import { ApiProperty } from '@nestjs/swagger';
import { EventTime } from '@src/DTO/eventTime';
import { IsNotEmpty, IsNumber, IsBoolean, IsOptional } from 'class-validator';
import { Type } from 'class-transformer';
import { isObject } from 'util';

/**
 * Model representing a request for creating an event
 */
export class CreateEventRequest {
    @IsNotEmpty()
    @ApiProperty()
    organization: string;

    @IsNotEmpty()
    @ApiProperty()
    @Type(() => EventTime)
    eventTime: EventTime;

    @IsNotEmpty()
    @ApiProperty()
    title: string;

    @IsNotEmpty()
    @ApiProperty()
    address: string;

    @IsNotEmpty()
    @ApiProperty()
    url: string;

    @ApiProperty()
    description: string;
    
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @ApiProperty()
    price?: number;

    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    @ApiProperty()
    isManual: boolean = false;

    @IsNumber()
    @IsNotEmpty()
    @ApiProperty()
    geocodeId: number;
}
