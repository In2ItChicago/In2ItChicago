import { json } from 'body-parser';
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { EventModule } from './event/event.module';
import { GeocodeModule } from './geocode/geocode.module';
import { GenericFilter } from './filters/generic.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(json({ limit: '50mb' }));
  app.enableCors();
  app.useGlobalFilters(new GenericFilter())
  app.useGlobalPipes(new ValidationPipe({transform: true, skipMissingProperties: true}))
  
  const options = new DocumentBuilder()
    .setTitle('Event API')
    .setDescription('Event API')
    .setVersion('1.0')
    .setSchemes(process.env.URL_SCHEME === 'https' ? 'https' : 'http')
    .build();

  const document = SwaggerModule.createDocument(app, options, {
    include: [AppModule, EventModule, GeocodeModule],
  });

  SwaggerModule.setup('/docs', app, document);
  await app.listen(5000);
}
bootstrap();
