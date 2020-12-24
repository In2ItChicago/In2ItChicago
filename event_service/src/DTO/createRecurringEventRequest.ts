import { ApiProperty } from '@nestjs/swagger';
import {
  IsNotEmpty,
  IsNumber,
  ValidateNested,
  Matches,
  IsOptional,
  IsBoolean,
} from 'class-validator';
import { Type } from 'class-transformer';
import { EventTime } from '@src/DTO/eventTime';

type Weekday =
  | 'Sunday'
  | 'Monday'
  | 'Tuesday'
  | 'Wednesday'
  | 'Thursday'
  | 'Friday'
  | 'Saturday';

export class CreateRecurringEventRequest {
  @IsNotEmpty()
  @ApiProperty()
  title: string;

  @ApiProperty()
  address: string | null;

  @ApiProperty()
  url: string;

  @IsNotEmpty()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty()
  price: number;

  @IsNotEmpty()
  @ApiProperty()
  description: string;

  @IsNotEmpty()
  @ApiProperty()
  @ValidateNested()
  @Type(() => EventTime)
  eventTime: EventTime;

  @IsOptional()
  @ApiProperty()
  organization: string;

  @Matches(/\b(week|dayOfMonth|weekOfMonth)\b/, {
    message: 'mode must be either "week", "dayOfMonth", or "weekOfMonth"',
  })
  @IsNotEmpty()
  @ApiProperty()
  mode: 'week' | 'dayOfMonth' | 'weekOfMonth';

  @IsOptional()
  @Matches(/\b(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\b/, {
    message: 'monthlyRecurringWeekday must be a valid day of the week',
  })
  @ApiProperty()
  monthlyRecurringWeekday: Weekday;

  @IsOptional()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty()
  monthlyRecurringWeekNumber: number;

  @IsOptional()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty()
  monthlyRecurringDay: number;

  @IsNotEmpty()
  @IsBoolean()
  @ApiProperty()
  @Type(() => Boolean)
  isHandicapAccessible: boolean;

  @IsNotEmpty()
  @IsBoolean()
  @Type(() => Boolean)
  @ApiProperty()
  requiresPhysicalActivities: boolean;

  @IsOptional()
  @ValidateNested({ each: true })
  @Matches(/\b(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\b/, {
    message: 'weeklyRecurringDays must contain valid days of the week',
    each: true,
  })
  @ApiProperty()
  weeklyRecurringDays: Weekday[];
}
