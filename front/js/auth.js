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
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await API.post('/auth/login', data);
        API.token = response.access_token;
        showToast('Login exitoso', 'success');
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 1000);
    } catch (error) {
        showToast(error.message, 'error');
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        await API.post('/users/register', data);
        showToast('Registro exitoso. Por favor inicia sesión.', 'success');
        toggleAuth('login');
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Check if already logged in
if (API.token) {
    window.location.href = 'dashboard.html';
}
