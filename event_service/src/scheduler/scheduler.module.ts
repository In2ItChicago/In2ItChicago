import { Module } from '@nestjs/common';
import { SchedulerService } from './scheduler.service';
import { SchedulerDALModule } from '@src/DAL/schedulerDAL.module';
import { SchedulerController } from './scheduler.controller';
import { SchedulerDAL } from '@src/DAL/schedulerDAL';

@Module({
  imports: [SchedulerDALModule],
  controllers: [SchedulerController],
  providers: [SchedulerService, SchedulerDAL]
})
export class SchedulerModule {
  constructor(private readonly schedulerService: SchedulerService) {}
}
