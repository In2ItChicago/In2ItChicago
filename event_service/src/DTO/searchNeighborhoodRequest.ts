import { ApiModelProperty } from "@nestjs/swagger";

export class SearchNeighborhoodRequest {
    @ApiModelProperty({required: false})
    neighborhood: string;
}