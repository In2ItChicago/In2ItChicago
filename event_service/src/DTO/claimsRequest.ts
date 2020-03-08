import { ApiProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsNotEmpty, IsBoolean, IsObject } from 'class-validator';
export class ClaimsRequest {
    @ApiProperty()
    email: string;

    @ApiProperty()
    @IsObject()
    claims: object;

    @ApiProperty()
    @IsBoolean()
    @IsNotEmpty()
    overwriteExisting: boolean;
}
