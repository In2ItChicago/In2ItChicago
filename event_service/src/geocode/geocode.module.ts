import { Module, HttpService, HttpModule } from '@nestjs/common';
import { GeocodeController } from './geocode.controller';
import { GeocodeService } from './geocode.service';
import { GeocodeDAL } from '../DAL/geocodeDAL';
import { GeocodeDALModule } from '@src/DAL/geocodeDAL.module';
import { EventDALModule } from '@src/DAL/eventDAL.module';
import { EventDAL } from '@src/DAL/eventDAL';

@Module({
    imports: [HttpModule, GeocodeDALModule, EventDALModule],
    controllers: [GeocodeController],
    providers: [GeocodeService, GeocodeDAL, EventDAL],
    exports: [GeocodeService],
})
export class GeocodeModule {
    constructor(private readonly geocodeService: GeocodeService) {}
}
