// Signup Form Validation
document.addEventListener("DOMContentLoaded", function () {
    let signupForm = document.getElementById("signupForm");
    let loginForm = document.getElementById("loginForm");

    // Signup Validation
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            let username = document.getElementById("signupUsername").value;
            let password = document.getElementById("signupPassword").value;

            if (username === "" || password === "") {
                alert("Username और Password खाली नहीं होने चाहिए!");
                event.preventDefault();
            } else if (password.length < 6) {
                alert("Password कम से कम 6 characters का होना चाहिए!");
                event.preventDefault();
            }
        });
    }

    // Login Validation
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            let username = document.getElementById("loginUsername").value;
            let password = document.getElementById("loginPassword").value;

            if (username === "" || password === "") {
                alert("Login के लिए Username और Password जरूरी है!");
                event.preventDefault();
            }
        });
    }
});
