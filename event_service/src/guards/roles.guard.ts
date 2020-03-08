import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { Observable } from 'rxjs';
import firebase from '@src/firebase/initialize';

@Injectable()
export class RolesGuard implements CanActivate {
    constructor(private readonly reflector: Reflector) {}

    async canActivate(context: ExecutionContext): Promise<boolean> {
        //console.log(context);
        // if (this.reflector) {
        //     return true;
        // }
        // return true;
        const roles = this.reflector.get<string[]>('roles', context.getHandler());
        console.log(roles);
        if (!roles) {
            return true;
        }
        const request = context.switchToHttp().getRequest();
        console.log(request.firebaseUser);
        for (let role of roles) {
            if (!request.firebaseUser[role]) {
                return false;
            }
        }
        //firebase.auth().getUser()
        
        //console.log(request);
        return true;//validateRequest(request);
    }
}