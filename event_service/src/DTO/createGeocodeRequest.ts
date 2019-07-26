import { ApiModelProperty } from '@nestjs/swagger';

export class CreateGeocodeRequest {
    @ApiModelProperty()
    address: string;
    @ApiModelProperty()
    lat: number;
    @ApiModelProperty()
    lon: number;
    @ApiModelProperty()
    neighborhood: string;
    @ApiModelProperty()
    expireAt?: Date;
}
