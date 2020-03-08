import { Controller, Get, Query, UseInterceptors, Post, Delete } from '@nestjs/common';
import { GeocodeService } from '@src/geocode/geocode.service';
import { GetGeocodeRequest } from '@src/DTO/getGeocodeRequest';
import { ApiTags, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { SearchNeighborhoodRequest } from '@src/DTO/searchNeighborhoodRequest';
import { Roles } from '@src/decorators/roles.decorator';

@ApiBearerAuth()
@ApiTags('geocode')
@Controller('geocode')
export class GeocodeController {
    constructor(private readonly geocodeService: GeocodeService) {}

    @Get()
    @ApiResponse({status: 200, type: GetGeocodeResponse, description: 'Geocode response'})
    async getGeocode(@Query() query: GetGeocodeRequest): Promise<GetGeocodeResponse> {
        return await this.geocodeService.getGeocode(query);
    }

    @Get('/all')
    @ApiResponse({status: 200, type: GetGeocodeResponse, isArray: true, description: 'All geocodes'})
    async getAllGeocodes(): Promise<GetGeocodeResponse[]> {
        return await this.geocodeService.getAllGeocodes();
    }

    @Get('/neighborhood')
    @ApiResponse({status: 200, type: GetGeocodeResponse, isArray: true, description: 'Geocodes matching neighborhood'})
    async neighborhoodSearch(@Query() query: SearchNeighborhoodRequest): Promise<GetGeocodeResponse[]> {
        return await this.geocodeService.searchNeighborhood(query);
    }

    @Get('/listNeighborhoods')
    @ApiResponse({status: 200, type: String, isArray: true, description: 'All available neighborhoods'})
    async listNeighborhoods(): Promise<String[]> {
        return await this.geocodeService.listNeighborhoods();
    }

    @Roles('systemAdmin')
    @Delete('/clearAllGeocodes')
    @ApiResponse({status: 200, description: 'Deleted'})
    async clear() {
        await this.geocodeService.clearAllGeocodes();
    }
}
