import { ApiModelProperty } from "@nestjs/swagger";
import { IsNotEmpty } from 'class-validator';

export class GetGeocodeRequest {
    @IsNotEmpty()
    @ApiModelProperty()
    address: string;
}