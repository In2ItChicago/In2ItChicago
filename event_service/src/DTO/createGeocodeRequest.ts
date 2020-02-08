import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsNumber, IsOptional } from 'class-validator';
import { Type } from 'class-transformer';
/**
 * Model for a Geocode creation request???
 */
export class CreateGeocodeRequest {
    @IsNotEmpty()
    @ApiProperty()
    address: string;

    @IsNumber()
    @Type(() => Number)
    @ApiProperty()
    lat: number;

    @IsNumber()
    @Type(() => Number)
    @ApiProperty()
    lon: number;

    @ApiProperty()
    neighborhood: string;
    
    @IsOptional()
    @ApiProperty()
    expireAt?: Date;
}
