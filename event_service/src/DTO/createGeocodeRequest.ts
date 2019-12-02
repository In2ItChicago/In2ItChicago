import { ApiModelProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsNumber } from 'class-validator';
import { Type } from 'class-transformer';
/**
 * Model for a Geocode creation request???
 */
export class CreateGeocodeRequest {
    @IsNotEmpty()
    @ApiModelProperty()
    address: string;

    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty()
    lat: number;

    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty()
    lon: number;

    @ApiModelProperty()
    neighborhood: string;
    
    @ApiModelProperty()
    expireAt?: Date;
}
