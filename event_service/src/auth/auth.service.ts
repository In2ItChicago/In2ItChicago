import { Injectable, HttpService } from '@nestjs/common';
import { AxiosResponse } from 'axios';
import { AuthRequest } from '@src/DTO/authRequest';
import firebase from '@src/firebase/initialize';
import { EmailRequest } from '@src/DTO/emailRequest';
import { ClaimsRequest } from '@src/DTO/claimsRequest';

@Injectable()
export class AuthService {
    constructor(private readonly httpService: HttpService) {}

    async login(authRequest: AuthRequest): Promise<string> {
        return this.auth('signInWithPassword', authRequest);
    }

    async createAccount(authRequest: AuthRequest) {
        return this.auth('signUp', authRequest);
    }

    async deleteAccount(emailRequest: EmailRequest) {
        const uid = await this.getUidFromEmail(emailRequest.email);
        await firebase.auth().deleteUser(uid);
    }

    async updateClaims(claimsRequest: ClaimsRequest): Promise<object> {
        const user = await firebase.auth().getUserByEmail(claimsRequest.email);
        let claims = claimsRequest.claims;
        if (!claimsRequest.overwriteExisting) {
            claims = Object.assign(user.customClaims, claims);
        }
        await firebase.auth().setCustomUserClaims(user.uid, claims);
        const newUser = await firebase.auth().getUser(user.uid);
        return newUser.customClaims;
    }

    async getUser(emailRequest: EmailRequest): Promise<object> {
        const user = await firebase.auth().getUserByEmail(emailRequest.email);
        return user;
    }

    async changePassword(authRequest: AuthRequest): Promise<object> {
        const uid = await this.getUidFromEmail(authRequest.email);
        const newUser = await firebase.auth().updateUser(uid, { password: authRequest.password});
        return newUser;
    }

    private async getUidFromEmail(email: string): Promise<string> {
        const user = await firebase.auth().getUserByEmail(email);
        return user.uid;
    }

    private async auth(path: string, authRequest: AuthRequest): Promise<string> {
        let res = await this.firebaseRequest(path,
            { email: authRequest.email, password: authRequest.password, returnSecureToken: true });

        return res.data.idToken;
    }

    private async firebaseRequest(path: string, data: object): Promise<AxiosResponse<any>> {
        return await this.httpService.post(`https://identitytoolkit.googleapis.com/v1/accounts:${path}?key=${process.env.FIREBASE_API_KEY}`, data).toPromise();
    }
}
