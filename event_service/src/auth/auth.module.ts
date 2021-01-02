import { Module, HttpService, HttpModule } from '@nestjs/common';
import { AuthController } from '@src/auth/auth.controller';
import { AuthService } from '@src/auth/auth.service';

@Module({
  imports: [HttpModule],
  controllers: [AuthController],
  providers: [AuthService],
  exports: [AuthService],
})
export class AuthModule {
  constructor(private readonly authService: AuthService) {}
}
