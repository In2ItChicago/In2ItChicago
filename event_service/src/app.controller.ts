import { Controller, Get, Post, Body } from '@nestjs/common';
import { AppService } from '@src/app.service';
import { AuthRequest } from '@src/DTO/authRequest';
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('/status')
  getStatus(): string {
    return this.appService.getStatus();
  }

  @Post('/auth')
  async auth(@Body() authRequest: AuthRequest): Promise<string> {
    return await this.appService.auth(authRequest);
  }
}
