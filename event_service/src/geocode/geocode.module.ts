import { Module, HttpService, HttpModule } from '@nestjs/common';
import { GeocodeController } from './geocode.controller';
import { GeocodeService } from './geocode.service';
import { GeocodeDAL } from '../DAL/geocodeDAL';
import { GeocodeDALModule } from '@src/DAL/geocodeDAL.module';

@Module({
    imports: [HttpModule, GeocodeDALModule],
    controllers: [GeocodeController],
    providers: [GeocodeService, GeocodeDAL],
    exports: [GeocodeService],
})
export class GeocodeModule {
    constructor(private readonly geocodeService: GeocodeService) {}
}
