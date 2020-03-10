import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { UserMetadata } from '@src/enums/userMetadata';

@Injectable()
export class OrganizationsGuard implements CanActivate {
    constructor(private readonly reflector: Reflector) {}

    async canActivate(context: ExecutionContext): Promise<boolean> {
        const request = context.switchToHttp().getRequest();
        const isEventAdmin = request.firebaseUser && request.firebaseUser[UserMetadata.EventAdmin];
        if (!(isEventAdmin || request?.firebaseUser?.allowedOrgs) || !request?.body?.events) {
            return false;
        }
        
        if (request.firebaseUser[UserMetadata.GodUser] || isEventAdmin) {
            return true;
        }

        return request.body.events.every(event => request.firebaseUser.allowedOrgs.includes(event.organization));
    }
}