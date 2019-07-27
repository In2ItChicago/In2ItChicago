import { Module } from '@nestjs/common';
import { GeocodeDAL } from './geocodeDAL';

@Module({
    providers: [{
        provide: 'GeocodeDAL',
        useValue: GeocodeDAL,
    }],
})
export class GeocodeDALModule {}
