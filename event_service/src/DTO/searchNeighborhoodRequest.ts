import { ApiProperty } from "@nestjs/swagger";
import { IsNotEmpty } from 'class-validator';

/**
 * Model for request a neighborhood search?????
 */
export class SearchNeighborhoodRequest {
    /**
     * The neighborhood to search for?? 
     */
    @IsNotEmpty()
    @ApiProperty()
    neighborhood: string;
}