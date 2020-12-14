import { ApiProperty } from '@nestjs/swagger';
import {
  IsNotEmpty,
  IsNumber,
  ValidateNested,
  Matches,
  IsOptional,
} from 'class-validator';
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

  @Matches(/week|dayOfMonth|weekOfMonth/, {
    message: 'mode must be either "week", "dayOfMonth", or "weekOfMonth"',
  })
  @IsNotEmpty()
  @ApiProperty()
  mode: 'week' | 'dayOfMonth' | 'weekOfMonth';

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
  @Type(() => Boolean)
  @ApiProperty()
  requiresPhysicalActivities: boolean;

  @ApiProperty()
  weeklyRecurringDays: string[];

  @IsOptional()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty()
  price?: number;
}
