import { json } from 'body-parser';
import { ValidationPipe } from '@src/pipes/validation.pipe';
import { NestFactory } from '@nestjs/core';
import { AppModule } from '@src/app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { EventModule } from '@src/event/event.module';
import { GeocodeModule } from '@src/geocode/geocode.module';
import { GenericFilter } from '@src/filters/generic.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(json({ limit: '50mb' }));
  app.enableCors();
  app.useGlobalFilters(new GenericFilter());
  app.useGlobalPipes(new ValidationPipe());

  var firebaseConfig = {
      apiKey: process.env.FIREBASE_API_KEY,
      authDomain: process.env.FIREBASE_AUTH_DOMAIN,
      databaseURL: process.env.FIREBASE_DATABASE_URL,
      projectId: process.env.FIREBASE_PROJECT_ID,
      storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
      messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
      appId: process.env.FIREBASE_APP_ID,
      measurementId: process.env.FIREBASE_MEASUREMENT_ID
  };
  
  const options = new DocumentBuilder()
    .addBearerAuth()
    .setTitle('Event API')
    .setDescription('Event API')
    .setVersion('1.0')
    .build();

  const document = SwaggerModule.createDocument(app, options, {
    include: [AppModule, EventModule, GeocodeModule],
  });

  SwaggerModule.setup('/docs', app, document);
  await app.listen(5000);
}
bootstrap();
