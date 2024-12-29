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

    $('#google-login-btn').on('click', function() {
        signInWithPopup(auth, provider)
            .then(function(result) {
                // Get the ID token from the result
                result.user.getIdToken().then(function(idToken) {
                    // Send token to flask backend using ajax
                    $.ajax({
                        url: '/auth/initialize',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({  id_token: idToken }),
                        success: function(response) {
                            if (response.status === 'success') {
                                window.location.href = '/admin/'
                            } else {
                                alert(response.message);
                            }
                        },
                        error: function() {
                            alert('Sign in failed try again');
                        }
                    });
                });
            }).catch(function() {
                alert('Failed to get Sigin Pop up!')
            });
    });

});