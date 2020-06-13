import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsNumber, IsOptional } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateRecurringEventRequest {
    @IsNotEmpty()
    @ApiProperty()
    title: string;

    @IsNotEmpty()
    @ApiProperty()
    address: string;

    @ApiProperty()
    url: string;

    @IsNumber()
    @Type(() => Number)
    @ApiProperty()
    cost: number;

    @IsNotEmpty()
    @ApiProperty()
    description: string;

    @IsNotEmpty()
    @ApiProperty()
    startDate: Date;

    @IsNotEmpty()
    @ApiProperty()
    endDate: Date;

    @IsNotEmpty()
    @ApiProperty()
    isHandicapAccessible: boolean;

    @IsNotEmpty()
    @ApiProperty()
    organization: string;

    @IsNotEmpty()
    @ApiProperty()
    isWeekly: boolean;

    @IsNotEmpty()
    @ApiProperty()
    isByWeekday: boolean;

    @ApiProperty()
    monthlyRecurringWeekday: string;

    @IsNumber()
    @Type(() => Number)
    @ApiProperty()
    monthlyRecurringWeekNumber: number;

    @IsNumber()
    @Type(() => Number)
    @ApiProperty()
    monthlyRecurringDay: number;

    @IsNotEmpty()
    @ApiProperty()
    requiresPhysicalActivities: boolean;

    @ApiProperty()
    weeklyRecurringDays: string[];
}