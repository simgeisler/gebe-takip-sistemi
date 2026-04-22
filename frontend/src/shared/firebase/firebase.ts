import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBhi671xnKRwgQzcb1g6qGDVLN1Bzje8kI",
  authDomain: "gebelik-takip-projesi.firebaseapp.com",
  projectId: "gebelik-takip-projesi",
  storageBucket: "gebelik-takip-projesi.firebasestorage.app",
  messagingSenderId: "120823291388",
  appId: "1:120823291388:web:edd9d34788a0943b40e679",
};

export const isFirebaseConfigured = !Object.values(firebaseConfig).some((value) => value === "FILL_ME");

const app = initializeApp(firebaseConfig);
export const firebaseAuth = getAuth(app);
