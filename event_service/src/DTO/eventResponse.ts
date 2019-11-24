import { ApiModelProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';

/**
 * Model for a single event returns from an events query
 */
export class EventResponse {
    /**
     * ID of the event.
     */
    @ApiModelProperty()
    id: number;

    /**
     * Title of the event.
     */
    @ApiModelProperty()
    title: string;

    /**
     * The external URL associated with this event.
     */
    @ApiModelProperty()
    url: string;

    /**
     * A description of this event.
     */
    @ApiModelProperty()
    description: string;

    /**
     * The organization which is holding the event
     */
    @ApiModelProperty()
    organization: string;

    /**
     * The cost of attending this event.
     */
    @ApiModelProperty()
    price: number;

    /**
     * The event start time.
     */
    @ApiModelProperty()
    startTime: string;

    /**
     * The event end time.
     */
    @ApiModelProperty()
    endTime: string;

    /**
     * What category? (categories?) does this event fall under?
     * Note: Should this be an enum or a list of enums? list of strings?
     */
    @ApiModelProperty()
    category: string;

    /**
     * The address of this event.
     */
    @ApiModelProperty()
    address: string;

    /**
     * The start date of this event.
     */
    @ApiModelProperty()
    startDate: string;

    /**
     * The end date of this event.
     */
    @ApiModelProperty()
    endDate: string;

    /**
     * The GeoCode latitude of this event.
     */
    @Type(() => Number)
    @ApiModelProperty()
    lat: number;
    
    /**
     * The GeoCode longitude of this event.
     */
    @Type(() => Number)
    @ApiModelProperty()
    lon: number;

    @Type(() => Number)
    @ApiModelProperty()
    score: number;
}
