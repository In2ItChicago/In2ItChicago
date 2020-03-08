import { ApiProperty } from '@nestjs/swagger';
export class EmailRequest {
    @ApiProperty()
    email: string;
}
