import { ApiModelProperty } from "@nestjs/swagger";
import { IsNotEmpty } from 'class-validator';

/**
 * Model for request a neighborhood search?????
 */
export class SearchNeighborhoodRequest {
    /**
     * The neighborhood to search for?? 
     */
    @IsNotEmpty()
    @ApiModelProperty()
    neighborhood: string;
}