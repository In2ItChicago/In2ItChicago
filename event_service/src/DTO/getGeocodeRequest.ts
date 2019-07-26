import { ApiModelProperty } from "@nestjs/swagger";

export class GetGeocodeRequest {
    @ApiModelProperty({required: false})
    address: string;
    @ApiModelProperty({required: false})
    neighborhood: string;
}