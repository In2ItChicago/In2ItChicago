import { Module, HttpModule, NestModule, MiddlewareConsumer, RequestMethod } from '@nestjs/common';
import { AppController } from '@src/app.controller';
import { AppService } from '@src/app.service';
import { GeocodeController } from '@src/geocode/geocode.controller';
import { EventController } from '@src/event/event.controller';
import { GeocodeService } from '@src/geocode/geocode.service';
import { EventService } from '@src/event/event.service';
import { GeocodeModule } from '@src/geocode/geocode.module';
import { EventModule } from '@src/event/event.module';
import { GeocodeDAL } from '@src/DAL/geocodeDAL';
import { GeocodeDALModule } from '@src/DAL/geocodeDAL.module';
import { EventDALModule } from '@src/DAL/eventDAL.module';
import { EventDAL } from '@src/DAL/eventDAL';

@Module({
  imports: [HttpModule, GeocodeModule, EventModule, GeocodeDALModule, EventDALModule],
  controllers: [GeocodeController, EventController, AppController],
  providers: [GeocodeService, EventService, AppService, GeocodeDAL, EventDAL],
})
export class AppModule {
  constructor(private readonly appService: AppService) {}
  
}
