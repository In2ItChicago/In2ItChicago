import { EventDAL } from '@src/DAL/eventDAL';
import { Module } from '@nestjs/common';

/**
 * What does DAL stand for? 
 */
@Module({
    providers: [{
        provide: 'EventDAL',
        useValue: EventDAL,
    }],
})
export class EventDALModule {}
