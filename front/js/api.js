const API_URL = '';

class API {
    static get token() {
        return localStorage.getItem('token');
    }

    static set token(value) {
        localStorage.setItem('token', value);
    }

    static logout() {
        localStorage.removeItem('token');
        window.location.href = '/front/login.html';
    }

    static async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            ...options,
            headers,
        };

        try {
            const response = await fetch(`${API_URL}${endpoint}`, config);

            if (response.status === 401) {
                this.logout();
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                let errorMessage = data.detail || 'Algo salió mal';

                // Handle Pydantic validation errors
                if (Array.isArray(data.detail)) {
                    const emailError = data.detail.find(err =>
                        err.loc && err.loc.includes('email') && err.type === 'value_error'
                    );

                    if (emailError) {
                        errorMessage = 'Por favor ingresa un correo electrónico válido (ejemplo: usuario@dominio.com)';
                    } else {
                        // Generic validation error message
                        errorMessage = data.detail.map(err => err.msg).join(', ');
                    }
                } else if (typeof errorMessage === 'object') {
                    errorMessage = JSON.stringify(errorMessage);
                }

                throw new Error(errorMessage);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    }

    static async get(endpoint) {
        return this.request(endpoint, {
            method: 'GET',
        });
    }
}

// Toast Notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    // Trigger reflow
    toast.offsetHeight;

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
