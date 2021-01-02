import { ApiProperty } from '@nestjs/swagger';
import { EventTime } from '@src/DTO/eventTime';
import {
  IsBoolean,
  IsNotEmpty,
  IsNotIn,
  IsNumber,
  IsOptional,
  ValidateNested,
} from 'class-validator';
import { Type } from 'class-transformer';
import { isBoolean } from 'validator';

/**
 * Model representing a request for creating an event
 */
export class CreateEventRequest {
  @IsNotEmpty()
  @ApiProperty()
  organization: string;

  @IsNotEmpty()
  @ApiProperty()
  @ValidateNested()
  @Type(() => EventTime)
  eventTime: EventTime;

  @IsNotEmpty()
  @ApiProperty()
  title: string;

  @IsNotIn([null, undefined])
  @ApiProperty()
  address: string;

  @IsNotIn([null, undefined])
  @ApiProperty()
  url: string;

  @IsNotEmpty()
  @ApiProperty()
  description: string;

  @IsNotEmpty()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty()
  price: number;

  @IsNotEmpty()
  @IsBoolean()
  @ApiProperty()
  @Type(() => Boolean)
  handicapAccessible: boolean;

  @IsNotEmpty()
  @IsBoolean()
  @Type(() => Boolean)
  @ApiProperty()
  requiresPhysicalActivities: boolean;
}
