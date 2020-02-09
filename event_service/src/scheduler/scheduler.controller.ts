import { Controller, Get, Query, UseInterceptors, Post, Delete } from '@nestjs/common';
import { ApiTags, ApiResponse } from '@nestjs/swagger';
import { SchedulerService } from './scheduler.service';

@ApiTags('scheduler')
@Controller('scheduler')
export class SchedulerController {
    constructor(private readonly schedulerService: SchedulerService) {}

    @Delete('/cleanupScheduler')
    @ApiResponse({status: 200, description: 'Deleted'})
    async cleanup() {
        await this.schedulerService.cleanupScheduler();
    }
}
