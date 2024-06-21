document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('SignIn');
    const emailField = document.getElementById('emailInput');
    const passwordField = document.getElementById('passwordInput');
    const inputFields = document.querySelectorAll('.input-field');

    loginButton.addEventListener('click', () => {
        inputFields.forEach(field => {
            if (field !== emailField && field !== passwordField) {
                field.classList.add('hidden');
            }
        });
    });
});
