import { Injectable, Inject } from '@nestjs/common';
import { SchedulerDAL } from '@src/DAL/schedulerDAL';

@Injectable()
export class SchedulerService {
    constructor(
        @Inject('SchedulerDAL') private readonly schedulerDAL: SchedulerDAL,
    ) { }

    async cleanupScheduler() {
        await this.schedulerDAL.cleanupScheduler();
    }
}
