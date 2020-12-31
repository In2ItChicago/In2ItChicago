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

    // No auth supplied
    if (!request.firebaseUser) {
      return false;
    }

    // God user or event admin can use any org
    if (
      request.firebaseUser[UserMetadata.GodUser] ||
      request.firebaseUser[UserMetadata.EventAdmin]
    ) {
      return true;
    }

    // If not an admin, user must be an event creator and have at least one org
    if (
      !request.firebaseUser[UserMetadata.EventCreator] ||
      !request.firebaseUser.allowedOrgs
    ) {
      return false;
    }

    // User is not an admin but can create, verify requested org is allowed
    if (request.body?.organization) {
      return request.firebaseUser.allowedOrgs.includes(
        request.body.organization,
      );
    }

    // organization parameter not in request
    return false;
  }
}
