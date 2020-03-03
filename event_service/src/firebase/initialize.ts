import * as admin from 'firebase-admin'

export default admin.initializeApp({
  credential: admin.credential.cert({
    projectId: process.env.FIREBASE_PROJECT_ID,
    privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
  }),
})

declare global {
  namespace Express {
    interface Request {
      firebaseUser: admin.auth.DecodedIdToken
    }
  }
}