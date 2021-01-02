import { ApiProperty } from '@nestjs/swagger';
import { IsDate } from 'class-validator';
import { Type } from 'class-transformer';

/**
 * Model representing an EventTime
 * Note: Why is this not being used in the other response or request models??
 */
export class EventTime {
  @IsDate()
  @Type(() => Date)
  @ApiProperty()
  startTimestamp: Date;

  @IsDate()
  @Type(() => Date)
  @ApiProperty()
  endTimestamp: Date;
}
