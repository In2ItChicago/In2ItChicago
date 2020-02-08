import { ApiProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';

/**
 * Model for a single event returns from an events query
 */
export class EventResponse {
    /**
     * ID of the event.
     */
    @ApiProperty()
    id: number;

    /**
     * Title of the event.
     */
    @ApiProperty()
    title: string;

    /**
     * The external URL associated with this event.
     */
    @ApiProperty()
    url: string;

    /**
     * A description of this event.
     */
    @ApiProperty()
    description: string;

    /**
     * The organization which is holding the event
     */
    @ApiProperty()
    organization: string;

    /**
     * The cost of attending this event.
     */
    @ApiProperty()
    price: number;

    /**
     * The event start time.
     */
    @ApiProperty()
    startTime: string;

    /**
     * The event end time.
     */
    @ApiProperty()
    endTime: string;

    /**
     * What category? (categories?) does this event fall under?
     * Note: Should this be an enum or a list of enums? list of strings?
     */
    @ApiProperty()
    category: string;

    /**
     * The address of this event.
     */
    @ApiProperty()
    address: string;

    /**
     * The start date of this event.
     */
    @ApiProperty()
    startDate: string;

    /**
     * The end date of this event.
     */
    @ApiProperty()
    endDate: string;

    /**
     * The GeoCode latitude of this event.
     */
    @Type(() => Number)
    @ApiProperty()
    lat: number;
    
    /**
     * The GeoCode longitude of this event.
     */
    @Type(() => Number)
    @ApiProperty()
    lon: number;

    /**
     * Score returned from text search ranking
     */
    @Type(() => Number)
    @ApiProperty()
    score: number;
}
