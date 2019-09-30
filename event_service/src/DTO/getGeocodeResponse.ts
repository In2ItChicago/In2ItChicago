import { ApiModelProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';

/**
 * Model for the response data returned by the GeoCode request.
 */
export class GetGeocodeResponse {
    /**
     * The ID of this request????
     */
    @ApiModelProperty()
    id: number;

    /**
     * The (normalized??) address returned by this request.
     */
    @ApiModelProperty()
    address: string;

    /**
     * The GeoCode latitude of the address.
     */
    @Type(() => Number)
    @ApiModelProperty()
    lat: number;

    /**
     * The GeoCode longitude of the address.
     */
    @Type(() => Number)
    @ApiModelProperty()
    lon: number;

    /**
     * The neighborhood of where this request occurs? 
     * Note: Should this be an enum? What if an event happens in many neighborhoods? 
     */
    @ApiModelProperty()
    neighborhood: string;
}
