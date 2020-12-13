import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsNumber, ValidateNested, Matches } from 'class-validator';
import { Type } from 'class-transformer';
import { EventTime } from '@src/DTO/eventTime';

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
  @ValidateNested()
  @Type(() => EventTime)
  eventTime: EventTime;

  @IsNotEmpty()
  @ApiProperty()
  isHandicapAccessible: boolean;

  @IsNotEmpty()
  @ApiProperty()
  organization: string;

  @Matches(/weekly|weekday/i, {
    message: 'mode must be either "weekly" or "weekday"',
  })
  @IsNotEmpty()
  @ApiProperty()
  mode: 'weekly' | 'weekday';

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
