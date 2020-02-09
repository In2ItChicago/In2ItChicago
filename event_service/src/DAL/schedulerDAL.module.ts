import { Module } from '@nestjs/common';
import { SchedulerDAL } from '@src/DAL/schedulerDAL';

@Module({
    providers: [{
        provide: 'SchedulerDAL',
        useValue: SchedulerDAL,
    }],
})
export class SchedulerDALModule {}
