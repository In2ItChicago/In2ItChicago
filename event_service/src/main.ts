import { json } from 'body-parser';
import * as csurf from 'csurf';
import * as helmet from 'helmet';
import * as rateLimit from 'express-rate-limit';
import { ValidationPipe } from '@src/pipes/validation.pipe';
import { NestFactory, Reflector } from '@nestjs/core';
import { NestExpressApplication } from '@nestjs/platform-express';
import { AppModule } from '@src/app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { EventModule } from '@src/event/event.module';
import { GeocodeModule } from '@src/geocode/geocode.module';
import { GenericFilter } from '@src/filters/generic.filter';
import { AuthModule } from '@src/auth/auth.module';
import { RolesGuard } from './guards/roles.guard';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);
  app.set('trust proxy', 1);
  app.use(helmet());
  app.use(json({ limit: '50mb' }));
  // TODO: use this for auth with cookies from ui?
  //app.use(csurf());
  app.enableCors();
  app.use(
    rateLimit({
      windowMs:  60 * 1000, // 1 minute
      max: 100, // limit each IP to 100 requests per windowMs
    }));
  app.useGlobalFilters(new GenericFilter());
  app.useGlobalPipes(new ValidationPipe());
  app.useGlobalGuards(new RolesGuard(new Reflector()));
  
  const options = new DocumentBuilder()
    .addBearerAuth()
    .setTitle('Event API')
    .setDescription('Event API')
    .setVersion('1.0')
    .build();

  const document = SwaggerModule.createDocument(app, options, {
    include: [AppModule, EventModule, GeocodeModule, AuthModule],
  });

  SwaggerModule.setup('/docs', app, document);
  await app.listen(5000);
}
bootstrap();
