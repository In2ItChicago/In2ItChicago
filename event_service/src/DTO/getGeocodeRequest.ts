import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsNumber, IsOptional } from 'class-validator';
import { Type } from 'class-transformer';
/**
 * Model representing a Geocode request??
 * (What does DTO stand for anyways???)
 */
export class GetGeocodeRequest {
  /**
   * The address a GeoCode is being requested for.
   */
  @ApiProperty()
  address: string | null;

  @IsOptional()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty({ required: false })
  lat?: number;

  @IsOptional()
  @IsNumber()
  @Type(() => Number)
  @ApiProperty({ required: false })
  lon?: number;
}
