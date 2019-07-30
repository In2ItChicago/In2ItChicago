import { ApiModelProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';

export class GetGeocodeResponse {
    @ApiModelProperty()
    id: number;

    @ApiModelProperty()
    address: string;

    @Type(() => Number)
    @ApiModelProperty()
    lat: number;

    @Type(() => Number)
    @ApiModelProperty()
    lon: number;
    
    @ApiModelProperty()
    neighborhood: string;
}
