import firebase from '@src/firebase/initialize';
import {
  Injectable,
  NestMiddleware,
  HttpStatus,
  RequestMethod,
} from '@nestjs/common';
import { RouteInfo } from '@nestjs/common/interfaces';
import { HttpException } from '@nestjs/common/exceptions/http.exception';
import { Request, Response } from 'express';

export const auth = (whitelist: RouteInfo[]) => (
  req: Request,
  res: Response,
  next: Function,
) => {
  // Remove query string
  const queryStringIndex = req.url.indexOf('?');
  const route =
    queryStringIndex > -1 ? req.url.substr(0, queryStringIndex) : req.url;

  // Skip auth for any routes in whitelist
  // Check if whitelist rule ends with *, then use startsWith comparison to allow
  if (
    whitelist.some(
      (routeInfo) =>
        req.method === RequestMethod[routeInfo.method] &&
        (routeInfo.path.endsWith('*')
          ? route.startsWith(
              routeInfo.path.substr(0, routeInfo.path.length - 1),
            )
          : route === routeInfo.path),
    )
  ) {
    next();
    return;
  }
  const { authorization } = req.headers;
  if (!authorization) {
    throw new HttpException(
      { message: 'No auth supplied' },
      HttpStatus.UNAUTHORIZED,
    );
  }
  const token = authorization.slice(7);

  try {
    firebase
      .auth()
      .verifyIdToken(token)
      .then((user) => {
        req.firebaseUser = user;
        next();
      })
      .catch((err) => {
        res.status(HttpStatus.UNAUTHORIZED).send('validation failed').end();
        // throw new HttpException(
        //   { message: 'Input data validation failed', err },
        //   HttpStatus.UNAUTHORIZED,
        // );
      });
  } catch (e) {
    throw e;
  }
};
