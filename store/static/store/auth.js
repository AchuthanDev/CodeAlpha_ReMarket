// store/static/store/auth.js

// --- Helper function to send token to Django backend ---
// --- Helper function to send token to Django backend ---
function sendTokenToBackend(token) {
    fetch('/firebase-login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Django login successful:', data.username);

            // --- THIS IS THE FIX ---
            // Only redirect if we are on the login or register page.
            const path = window.location.pathname;
            if (path.includes('/login/') || path.includes('/register/')) {
                window.location.href = '/'; // Redirect to homepage
            }
            // If we're on any other page, do nothing. The page just loads.

        } else {
            console.error('Django login failed:', data.message);
            auth.signOut(); // Sign out from Firebase if Django login fails
        }
    })
    .catch(error => {
        console.error('Error sending token to backend:', error);
        auth.signOut();
    });
}
// --- Main Auth Listener ---
// This runs when the page loads and whenever the auth state changes
auth.onAuthStateChanged(user => {
    if (user) {
        // User is signed in (either just now or from a previous session)
        console.log('Firebase user logged in:', user.email);

        // Get the ID token
        user.getIdToken().then(token => {
            // Send this token to our Django backend to log in the Django user
            sendTokenToBackend(token);
        });

    } else {
        // User is signed out
        console.log('Firebase user logged out.');
    }
});

// --- Google Sign-In ---
function signInWithGoogle() {
    auth.signInWithPopup(googleProvider)
        .catch(error => {
            console.error('Google Sign-In Error:', error.message);
        });
}

// --- Email/Password Sign-Up ---
function signUpWithEmail(email, password) {
    auth.createUserWithEmailAndPassword(email, password)
        .catch(error => {
            alert('Sign-up Error: ' + error.message);
        });
}

// --- Email/Password Sign-In ---
function signInWithEmail(email, password) {
    auth.signInWithEmailAndPassword(email, password)
        .catch(error => {
            alert('Login Error: ' + error.message);
        });
}

// --- Sign-Out ---
// --- Sign-Out ---
function signOut() {
    auth.signOut().then(() => {
        // After Firebase is signed out,
        // redirect to Django's logout URL to clear the Django session.
        window.location.href = '/logout/';
    }).catch((error) => {
        console.error('Sign-out error:', error);
    });
}