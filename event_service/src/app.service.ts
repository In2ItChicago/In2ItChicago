import { Injectable, HttpService } from '@nestjs/common';

@Injectable()
export class AppService {
  constructor(private readonly httpService: HttpService) {}

  getStatus(): string {
    return 'Success';
  }
}
