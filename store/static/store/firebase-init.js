
const firebaseConfig = {
  apiKey: "AIzaSyA-KHMhVR9miYZugC_ayz2V0kNoNx51TWY",
  authDomain: "remarket-a4d0d.firebaseapp.com",
  projectId: "remarket-a4d0d",
  storageBucket: "remarket-a4d0d.firebasestorage.app",
  messagingSenderId: "37194412136",
  appId: "1:37194412136:web:7f879a0e9fd4529980cbdd",
  measurementId: "G-16H8W5MVT1"
};


// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const googleProvider = new firebase.auth.GoogleAuthProvider();