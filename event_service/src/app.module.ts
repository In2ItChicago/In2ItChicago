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
import { SchedulerController } from '@src/scheduler/scheduler.controller';
import { SchedulerModule } from '@src/scheduler/scheduler.module';
import { SchedulerService } from '@src/scheduler/scheduler.service';
import { SchedulerDAL } from '@src/DAL/schedulerDAL';
import { AuthController } from '@src/auth/auth.controller';
import { AuthService } from '@src/auth/auth.service';
import { AuthModule } from '@src/auth/auth.module';

@Module({
  imports: [HttpModule, GeocodeModule, EventModule, GeocodeDALModule, EventDALModule, SchedulerModule, AuthModule],
  controllers: [GeocodeController, EventController, AppController, SchedulerController, AuthController],
  providers: [GeocodeService, EventService, AppService, SchedulerService, GeocodeDAL, EventDAL, SchedulerDAL, AuthService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {}
  constructor(private readonly appService: AppService) {}
}
