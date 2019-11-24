import { Test, TestingModule } from '@nestjs/testing';
import { GeocodeService } from '@src/geocode/geocode.service';

describe('GeocodeService', () => {
  let service: GeocodeService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [GeocodeService],
    }).compile();

    service = module.get<GeocodeService>(GeocodeService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
