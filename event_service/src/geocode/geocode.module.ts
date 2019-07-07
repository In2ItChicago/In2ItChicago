import { Module, HttpService, HttpModule } from '@nestjs/common';
import { GeocodeController } from './geocode.controller';
import { GeocodeService } from './geocode.service';
import { GeocodeDAL } from '../DAL/geocodeDAL';

Module({
    imports: [HttpModule],
    controllers: [GeocodeController],
    providers: [GeocodeService],
    exports: [GeocodeService],
});

export class GeocodeModule {
    constructor(private readonly geocodeService: GeocodeService) {}
}
