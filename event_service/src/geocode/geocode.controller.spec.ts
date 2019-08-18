import { Test, TestingModule } from '@nestjs/testing';
import { GeocodeController } from './geocode.controller';

describe('Geocode Controller', () => {
  let controller: GeocodeController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [GeocodeController],
    }).compile();

    controller = module.get<GeocodeController>(GeocodeController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
