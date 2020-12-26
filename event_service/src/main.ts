import { json } from 'body-parser';
import * as csurf from 'csurf';
import * as helmet from 'helmet';
import * as rateLimit from 'express-rate-limit';
import { ValidationPipe } from '@src/pipes/validation.pipe';
import { NestFactory, Reflector } from '@nestjs/core';
import { RequestMethod } from '@nestjs/common';
import { NestExpressApplication } from '@nestjs/platform-express';
import { AppModule } from '@src/app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { EventModule } from '@src/event/event.module';
import { GeocodeModule } from '@src/geocode/geocode.module';
import { GenericFilter } from '@src/filters/generic.filter';
import { AuthModule } from '@src/auth/auth.module';
import { RolesGuard } from './guards/roles.guard';
import { auth } from '@src/middleware/auth.middleware';

async function bootstrap() {
  const isDev = process.env.NODE_ENV === 'development';
  const bypassAuth = process.env.BYPASS_AUTH === '1' && isDev;
  const app = await NestFactory.create<NestExpressApplication>(AppModule);
  app.set('trust proxy', 1);
  app.use(helmet());
  app.use(json({ limit: '50mb' }));
  app.enableCors({
    origin: isDev
      ? ['http://localhost', 'http://localhost:3000']
      : 'https://in2itchicago.com',
  });
  // The supplied parameters are the whitelist of routes not to authorize
  // Otherwise, any route requires auth by default
  if (bypassAuth) {
    app.use(
      auth([
        { method: RequestMethod.OPTIONS, path: '/*' },
        { method: RequestMethod.GET, path: '/*' },
        { method: RequestMethod.POST, path: '/*' },
        { method: RequestMethod.DELETE, path: '/*' },
        { method: RequestMethod.PUT, path: '/*' },
        { method: RequestMethod.PATCH, path: '/*' },
      ]),
    );
  } else {
    app.use(
      auth([
        // OPTIONS request don't use auth per the CORS spec
        { method: RequestMethod.OPTIONS, path: '/*' },
        { method: RequestMethod.GET, path: '/' },
        { method: RequestMethod.GET, path: '/docs*' },
        { method: RequestMethod.GET, path: '/geocode*' },
        { method: RequestMethod.GET, path: '/events' },
        { method: RequestMethod.GET, path: '/status' },
        { method: RequestMethod.POST, path: '/auth/login' },
      ]),
    );
  }

  // TODO: use this for auth with cookies from ui?
  //app.use(csurf());

  // TODO: maybe use Caddy to do this instead
  // app.use(
  //   rateLimit({
  //     windowMs:  5 * 60 * 1000, // 1 minute
  //     max: 5000
  //   }));
  app.useGlobalFilters(new GenericFilter());
  app.useGlobalPipes(new ValidationPipe());

  if (!bypassAuth) {
    app.useGlobalGuards(new RolesGuard(new Reflector()));
  }

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
