function toggleAuth(mode) {
    const loginCard = document.getElementById('login-card');
    const registerCard = document.getElementById('register-card');

    if (mode === 'register') {
        loginCard.classList.add('hidden');
        registerCard.classList.remove('hidden');
    } else {
        registerCard.classList.add('hidden');
        loginCard.classList.remove('hidden');
    }
}


document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    const errorDiv = document.getElementById('login-error');

    // Reset state
    errorDiv.classList.add('hidden');
    errorDiv.classList.remove('success');
    errorDiv.textContent = '';
    btn.classList.add('btn-loading');

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await API.post('/auth/login', data);
        API.token = response.access_token;
        // Keep loading state during redirect
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 500);
    } catch (error) {
        btn.classList.remove('btn-loading');
        errorDiv.textContent = error.message || 'Error al iniciar sesión';
        errorDiv.classList.remove('hidden');
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    const errorDiv = document.getElementById('register-error');

    // Reset state
    errorDiv.classList.add('hidden');
    errorDiv.textContent = '';
    btn.classList.add('btn-loading');

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        await API.post('/users/register', data);

        // Switch to login
        toggleAuth('login');

        // Show success message in login form
        const loginErrorDiv = document.getElementById('login-error');
        loginErrorDiv.textContent = 'Registro exitoso. Por favor inicia sesión.';
        loginErrorDiv.classList.remove('hidden');
        loginErrorDiv.classList.add('success');

        btn.classList.remove('btn-loading');
    } catch (error) {
        btn.classList.remove('btn-loading');
        errorDiv.textContent = error.message || 'Error al registrarse';
        errorDiv.classList.remove('hidden');
        errorDiv.classList.remove('success');
    }
});

// Check if already logged in
if (API.token) {
    window.location.href = 'dashboard.html';
}
