// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getStorage } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAPy1XDc4eSCb14O5lZaFm4vtq6s-0lKyg",
  authDomain: "fir-storage-1cc71.firebaseapp.com",
  projectId: "fir-storage-1cc71",
  storageBucket: "fir-storage-1cc71.appspot.com",
  messagingSenderId: "137355443807",
  appId: "1:137355443807:web:d346a85c0bf3831b9265ea",
  measurementId: "G-TWNSZ0REFG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

const storage = getStorage(app, firebaseConfig.storageBucket);

export { storage, analytics as default };