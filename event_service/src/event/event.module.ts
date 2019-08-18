import { Module, HttpService, HttpModule } from '@nestjs/common';
import { EventController } from './event.controller';
import { EventService } from './event.service';
import { GeocodeModule } from '@src/geocode/geocode.module';
import { GeocodeService } from '@src/geocode/geocode.service';
import { GeocodeDAL } from '@src/DAL/geocodeDAL';
import { GeocodeDALModule } from '@src/DAL/geocodeDAL.module';
import { EventDALModule } from '@src/DAL/eventDAL.module';
import { EventDAL } from '@src/DAL/eventDAL';

@Module({
    imports: [HttpModule, GeocodeModule, EventDALModule, GeocodeDALModule],
    controllers: [EventController],
    providers: [GeocodeService, EventService, EventDAL, GeocodeDAL],
    exports: [EventService],
})
export class EventModule {
    constructor(private readonly eventService: EventService) {}
}
