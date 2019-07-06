import { Module } from '@nestjs/common';
import { EventController } from './event.controller';
import { EventService } from './event.service';
import { GeocodeModule } from 'src/geocode/geocode.module';

@Module({
    imports: [GeocodeModule],
    controllers: [EventController],
    providers: [EventService],
    exports: [EventService],
})
export class EventModule {
    constructor(private readonly eventService: EventService) {}
}
