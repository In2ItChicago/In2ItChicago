import * as admin from 'firebase-admin';

export default process.env.BYPASS_AUTH === '1'
  ? null
  : admin.initializeApp({
      credential: admin.credential.cert({
        projectId: process.env.FIREBASE_PROJECT_ID,
        privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n')
          .split('%20')
          .join(' '),
        clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      }),
      serviceAccountId: process.env.FIREBASE_CLIENT_EMAIL,
    });

declare global {
  namespace Express {
    interface Request {
      firebaseUser: admin.auth.DecodedIdToken;
    }
  }
}
