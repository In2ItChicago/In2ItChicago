import { ApiProperty } from '@nestjs/swagger';
import { EventTime } from '@src/DTO/eventTime';
import {
  IsBoolean,
  IsNotEmpty,
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

  @ApiProperty()
  address: string;

  @IsNotEmpty()
  @ApiProperty()
  url: string;

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
