import { EventDAL } from './eventDAL';
import { Module } from '@nestjs/common';

@Module({
    providers: [{
        provide: 'EventDAL',
        useValue: EventDAL,
    }],
})
export class EventDALModule {}
