import { ApiModelProperty } from "@nestjs/swagger";

export class GetGeocodeRequest {
    @ApiModelProperty()
    address: string;
    @ApiModelProperty()
    neighborhood: string;
}