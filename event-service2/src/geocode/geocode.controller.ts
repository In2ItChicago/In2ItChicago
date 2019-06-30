import { Controller } from '@nestjs/common';
import { GeocodeService } from './geocode.service';

@Controller('geocode')
export class GeocodeController {
    constructor(private readonly geocodeService: GeocodeService) {}
}
