// Check auth
if (!API.token) {
    window.location.href = 'index.html';
}

// Profile Modal Logic
const profileModal = document.getElementById('profile-modal');
let currentUser = null;

// Load User Info
async function loadUser() {
    try {
        const user = await API.get('/users/me');
        currentUser = user;
        document.getElementById('user-name').textContent = user.full_name;
    } catch (error) {
        console.error('Error loading user:', error);
    }
}

function openProfileModal() {
    if (!currentUser) return;
    document.getElementById('profile-id').value = currentUser.id;
    document.getElementById('profile-name').value = currentUser.full_name;
    document.getElementById('profile-email').value = currentUser.email;
    profileModal.classList.remove('hidden');
}

function closeProfileModal() {
    profileModal.classList.add('hidden');
}

// Close modal on click outside (for profileModal)
profileModal.addEventListener('click', (e) => {
    if (e.target === profileModal) closeProfileModal();
});

// Load Groups
async function loadGroups() {
    const grid = document.getElementById('groups-grid');
    grid.innerHTML = '<p class="text-muted">Cargando grupos...</p>';

    try {
        const groups = await API.get('/groups/my-groups');

        if (groups.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; background: var(--card-bg); border-radius: 1rem; border: 1px dashed var(--border-color);">
                    <h3>No tienes grupos aún</h3>
                    <p class="text-muted mb-4">Crea uno para empezar a dividir gastos</p>
                    <button onclick="openCreateGroupModal()" class="btn btn-primary">Crear Grupo</button>
                </div>
            `;
            return;
        }

        grid.innerHTML = groups.map(group => `
            <div class="card group-card" onclick="window.location.href='group.html?id=${group.id}'">
                <h3 style="margin-bottom: 0.5rem;">${group.name}</h3>
                <p class="text-muted" style="font-size: 0.875rem;">
                    Creado por ${group.owner_name || 'User #' + group.created_by}
                </p>
            </div>
        `).join('');
    } catch (error) {
        grid.innerHTML = `<p style="color: var(--error-color)">Error al cargar grupos: ${error.message}</p>`;
    }
}

// Modal Logic
const modal = document.getElementById('create-group-modal');

function openCreateGroupModal() {
    modal.classList.remove('hidden');
}

function closeCreateGroupModal() {
    modal.classList.add('hidden');
    document.getElementById('create-group-form').reset();
}

// Create Group
document.getElementById('create-group-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        await API.post('/groups/', data);
        showToast('Grupo creado exitosamente', 'success');
        closeCreateGroupModal();
        loadGroups();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Close modal on click outside
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeCreateGroupModal();
});

// Init
loadUser();
loadGroups();
