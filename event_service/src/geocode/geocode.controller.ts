import { Controller, Get, Query, Post } from '@nestjs/common';
import { GeocodeService } from './geocode.service';
import { GetGeocodeRequest } from '../../src/DTO/getGeocodeRequest';

@Controller('geocode')
export class GeocodeController {
    constructor(private readonly geocodeService: GeocodeService) {}

    @Get()
    async getGeocode(@Query() query: GetGeocodeRequest) {
        return await this.geocodeService.getGeocode(query);
    }
}
