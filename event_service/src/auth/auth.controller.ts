import { Controller, Post, Body, Delete, Query, Get } from '@nestjs/common';
import { ApiTags, ApiBody, ApiResponse, ApiBearerAuth, ApiBasicAuth } from '@nestjs/swagger';
import { AuthService } from '@src/auth/auth.service';
import { AuthRequest } from '@src/DTO/authRequest';
import { EmailRequest } from '@src/DTO/emailRequest';
import { ClaimsRequest } from '@src/DTO/claimsRequest';
import { Roles } from '@src/decorators/roles.decorator';

@ApiBearerAuth()
@Controller('auth')
@ApiTags('auth')
export class AuthController {
    constructor(private readonly authService: AuthService) {}

    @Roles('userAdmin')
    @Get('/user')
    async getUser(@Query() emailRequest: EmailRequest): Promise<object> {
        const user = await this.authService.getUser(emailRequest);
        return user;
    }

    @Post('/login')
    async login(@Body() authRequest: AuthRequest): Promise<string> {
        const token = await this.authService.login(authRequest);
        return token;
    }

    @Roles('userAdmin')
    @Post('/createAccount')
    async createAccount(@Body() authRequest: AuthRequest): Promise<string> {
        const token = await this.authService.createAccount(authRequest);
        return token;
    }

    @Roles('userAdmin')
    @Post('/updateClaims')
    async updateClaims(@Body() claimsRequest: ClaimsRequest): Promise<object> {
        const claims = await this.authService.updateClaims(claimsRequest);
        return claims;
    }

    @Roles('userAdmin')
    @Post('/changePassword')
    async changePassword(@Body() authRequest: AuthRequest): Promise<object> {
        const newUser = this.authService.changePassword(authRequest);
        return newUser;
    }

    @Roles('userAdmin')
    @Delete('/deleteAccount')
    async deleteAccount(@Query() emailRequest: EmailRequest) {
        await this.authService.deleteAccount(emailRequest);
    }
}
