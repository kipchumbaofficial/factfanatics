/**Handles firebase login
*/

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.12.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/9.12.0/firebase-auth.js";


$(document).ready(function() {
    // Firebase configuration
    const firebaseConfig = {
        apiKey: "AIzaSyA3PDM_U-GxS7i_BlIrZq1HnHGmo3vn644",
        authDomain: "fact-fanatics.firebaseapp.com",
        projectId: "fact-fanatics",
        storageBucket: "fact-fanatics.firebasestorage.app",
        messagingSenderId: "812458840032",
        appId: "1:812458840032:web:dfba0a59f5290e6d262585"
    };

    // Initialize Firebase
    const app = initializeApp(firebaseConfig);

    // Initialize Firebase Auth
    const auth = getAuth(app);
    const provider = new GoogleAuthProvider();

    // Store the current URL before login (in case user is redirected)
    const currentUrl = window.location.href;
    localStorage.setItem('redirectUrl', currentUrl);

    $('#google-login-btn').on('click', function() {
        signInWithPopup(auth, provider)
            .then(function(result) {
                // Get the ID token from the result
                result.user.getIdToken().then(function(idToken) {
                    // Send token to Flask backend using Ajax
                    $.ajax({
                        url: '/auth/login',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ id_token: idToken }),
                        success: function(response) {
                            if (response.status === 'success') {
                                // Redirect to the stored URL or default to admin
                                const redirectUrl = localStorage.getItem('redirectUrl') || '/admin/';
                                window.location.href = redirectUrl;
                                localStorage.removeItem('redirectUrl'); // Clear redirect URL
                            } else {
                                alert(response.message);
                            }
                        },
                        error: function() {
                            alert('Sign in failed, try again');
                        }
                    });
                });
            }).catch(function() {
                alert('Failed to get Sign In Pop up!');
            });
    });
});
