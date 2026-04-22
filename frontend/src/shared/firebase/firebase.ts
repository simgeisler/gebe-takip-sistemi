import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "FILL_ME",
  authDomain: "FILL_ME",
  projectId: "FILL_ME",
  storageBucket: "FILL_ME",
  messagingSenderId: "FILL_ME",
  appId: "FILL_ME",
};

export const isFirebaseConfigured = !Object.values(firebaseConfig).some((value) => value === "FILL_ME");

const app = initializeApp(firebaseConfig);
export const firebaseAuth = getAuth(app);
