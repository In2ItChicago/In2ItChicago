import firebase from 'firebase'

let env = null;
if (Object.keys(process.env).length > 0) {
    env = process.env;
}
else {
    env = window.__NUXT__.env;
}
var firebaseConfig = {
    apiKey: env.FIREBASE_API_KEY,
    authDomain: env.FIREBASE_AUTH_DOMAIN,
    databaseURL: env.FIREBASE_DATABASE_URL,
    projectId: env.FIREBASE_PROJECT_ID,
    storageBucket: env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: env.FIREBASE_MESSAGING_SENDER_ID,
    appId: env.FIREBASE_APP_ID,
    measurementId: env.FIREBASE_MEASUREMENT_ID
};

  // Initialize Firebase
const app = firebase.apps.length
    ? firebase.app()
    : firebase.initializeApp(firebaseConfig);
//firebase.analytics();
export const db = app.database();