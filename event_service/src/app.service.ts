import { Injectable, HttpService } from '@nestjs/common';
import * as firebase from 'firebase';
import * as admin from 'firebase-admin'
import { AuthRequest } from '@src/DTO/authRequest';

@Injectable()
export class AppService {
  constructor(private readonly httpService: HttpService) {}

  async auth(authRequest: AuthRequest) {
    // await firebase.auth().signInWithEmailAndPassword(authRequest.email, authRequest.password);
    // let token = await firebase.auth().currentUser.getIdToken();
    // return token;
    let token = await admin.auth().createCustomToken(authRequest.email);
    console.log(process.env.FIREBASE_API_KEY);
    let res = await this.httpService.post(`https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=${process.env.FIREBASE_API_KEY}`, 
    { token, returnSecureToken: true }).toPromise();
    console.log(res.data);
    return res.data.idToken;
  }

  getStatus(): string {
    return 'Success';
  }
}
