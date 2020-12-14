import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { UserMetadata } from '@src/enums/userMetadata';

@Injectable()
export class OrganizationsGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    if (
      process.env.BYPASS_AUTH === '1' &&
      process.env.NODE_ENV === 'development'
    ) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const isEventAdmin =
      request.firebaseUser && request.firebaseUser[UserMetadata.EventAdmin];
    if (!(isEventAdmin || request?.firebaseUser?.allowedOrgs)) {
      return false;
    }

    if (request.firebaseUser[UserMetadata.GodUser] || isEventAdmin) {
      return true;
    }
    if (request.body?.events) {
      return request.body.events.every((event) =>
        request.firebaseUser.allowedOrgs.includes(event.organization),
      );
    }
    if (request.body?.event) {
      return request.firebaseUser.allowedOrgs.includes(
        request.body.event.organization,
      );
    }
  }
}
