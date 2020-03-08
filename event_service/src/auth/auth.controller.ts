import { Controller, Post, Body, Delete, Query } from '@nestjs/common';
import { ApiTags, ApiBody, ApiResponse, ApiBearerAuth, ApiBasicAuth } from '@nestjs/swagger';
import { AuthService } from '@src/auth/auth.service';
import { AuthRequest } from '@src/DTO/authRequest';
import { EmailRequest } from '@src/DTO/emailRequest';
import { ClaimsRequest } from '@src/DTO/claimsRequest';

@Controller('auth')
@ApiTags('auth')
export class AuthController {
    constructor(private readonly authService: AuthService) {}

    @Post('/login')
    async login(@Body() authRequest: AuthRequest): Promise<string> {
        const token = await this.authService.login(authRequest);
        return token;
    }

    @Post('/createAccount')
    async createAccount(@Body() authRequest: AuthRequest): Promise<string> {
        const token = await this.authService.createAccount(authRequest);
        return token;
    }

    @Post('/updateClaims')
    async updateClaims(@Body() claimsRequest: ClaimsRequest): Promise<object> {
        const claims = await this.authService.updateClaims(claimsRequest);
        return claims;
    }

    @Delete('/deleteAccount')
    async deleteAccount(@Query() emailRequest: EmailRequest) {
        await this.authService.deleteAccount(emailRequest);
    }
}
