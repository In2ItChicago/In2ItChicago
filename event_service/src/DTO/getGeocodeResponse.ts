import { ApiModelProperty } from '@nestjs/swagger';

export class GetGeocodeResponse {
    @ApiModelProperty()
    address: string;
    @ApiModelProperty()
    lat: string;
    @ApiModelProperty()
    lon: string;
    @ApiModelProperty()
    neighborhood: string;
}
