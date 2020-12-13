import { ApiProperty } from '@nestjs/swagger';
import { EventTime } from '@src/DTO/eventTime';
import {
  IsNotEmpty,
  IsNumber,
  IsOptional,
  ValidateNested,
} from 'class-validator';
import { Type } from 'class-transformer';

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
}
