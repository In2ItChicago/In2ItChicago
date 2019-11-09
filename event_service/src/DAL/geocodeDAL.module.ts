import { Module } from '@nestjs/common';
import { GeocodeDAL } from '@src/DAL/geocodeDAL';

@Module({
    providers: [{
        provide: 'GeocodeDAL',
        useValue: GeocodeDAL,
    }],
})
export class GeocodeDALModule {}
