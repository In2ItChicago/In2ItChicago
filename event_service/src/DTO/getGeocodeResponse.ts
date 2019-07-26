import { ApiModelProperty } from '@nestjs/swagger';

export class GetGeocodeResponse {
    @ApiModelProperty()
    id: number;
    @ApiModelProperty()
    address: string;
    @ApiModelProperty()
    lat: number;
    @ApiModelProperty()
    lon: number;
    @ApiModelProperty()
    neighborhood: string;
}
