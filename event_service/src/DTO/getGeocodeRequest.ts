import { ApiModelProperty } from "@nestjs/swagger";
import { IsNotEmpty } from 'class-validator';

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
}