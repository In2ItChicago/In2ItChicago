import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GeocodeController } from './geocode/geocode.controller';
import { EventController } from './event/event.controller';
import { GeocodeService } from './geocode/geocode.service';
import { EventService } from './event/event.service';
import { GeocodeModule } from './geocode/geocode.module';
import { EventModule } from './event/event.module';

@Module({
  imports: [GeocodeModule, EventModule],
  controllers: [AppController, GeocodeController, EventController],
  providers: [AppService, GeocodeService, EventService],
})
export class AppModule {}
