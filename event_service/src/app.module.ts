import { Module, HttpModule, HttpService } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GeocodeController } from './geocode/geocode.controller';
import { EventController } from './event/event.controller';
import { GeocodeService } from '../src/geocode/geocode.service';
import { EventService } from './event/event.service';
import { GeocodeModule } from './geocode/geocode.module';
import { EventModule } from './event/event.module';

@Module({
  imports: [HttpModule, GeocodeModule, EventModule],
  controllers: [GeocodeController, EventController, AppController],
  providers: [GeocodeService, EventService, AppService],
})
export class AppModule {
  constructor(private readonly appService: AppService) {}
}
