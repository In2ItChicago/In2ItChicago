import { ApiModelProperty } from "@nestjs/swagger";
import { IsNotEmpty } from 'class-validator';

export class SearchNeighborhoodRequest {
    @IsNotEmpty()
    @ApiModelProperty()
    neighborhood: string;
}