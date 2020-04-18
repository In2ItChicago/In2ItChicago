import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { UserMetadata } from '@src/enums/userMetadata';

@Injectable()
export class RolesGuard implements CanActivate {
    constructor(private readonly reflector: Reflector) {}

    async canActivate(context: ExecutionContext): Promise<boolean> {
        const roles = this.reflector.get<UserMetadata[]>('roles', context.getHandler());
        
        if (!roles) {
            return true;
        }
        // godUser can do anything
        const checkRoles = roles.concat([UserMetadata.GodUser]);
        const request = context.switchToHttp().getRequest();
        if (!request.firebaseUser) {
            return false;
        }
        
        return checkRoles.some(role => request.firebaseUser[role]);
    }
}