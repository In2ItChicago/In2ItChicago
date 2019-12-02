import { ApiModelProperty } from "@nestjs/swagger";
import { IsNotEmpty, IsNumber } from 'class-validator';
import { Type } from 'class-transformer';
/**
 * Model representing a Geocode request??
 * (What does DTO stand for anyways???)
 */
export class GetGeocodeRequest {
    /**
     * The address a GeoCode is being requested for.
     */
    @IsNotEmpty()
    @ApiModelProperty()
    address: string;

    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty({required: false})
    lat?: number;

    @IsNumber()
    @Type(() => Number)
    @ApiModelProperty({required: false})
    lon?: number;
}