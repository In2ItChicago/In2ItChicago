import { Controller, Get, Query, UseInterceptors, Post, Delete } from '@nestjs/common';
import { ApiTags, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { SchedulerService } from './scheduler.service';
import { Roles } from '@src/decorators/roles.decorator';
import { UserMetadata } from '@src/enums/userMetadata';

@ApiBearerAuth()
@ApiTags('scheduler')
@Controller('scheduler')
export class SchedulerController {
    constructor(private readonly schedulerService: SchedulerService) {}

    @Roles(UserMetadata.SystemAdmin)
    @Delete('/cleanupScheduler')
    @ApiResponse({status: 200, description: 'Deleted'})
    async cleanup() {
        await this.schedulerService.cleanupScheduler();
    }
}
