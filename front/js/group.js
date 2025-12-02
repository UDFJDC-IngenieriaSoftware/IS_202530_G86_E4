// Check auth
if (!API.token) {
    window.location.href = 'index.html';
}

const urlParams = new URLSearchParams(window.location.search);
const groupId = urlParams.get('id');

if (!groupId) {
    window.location.href = 'dashboard.html';
}

let currentMembers = [];

// Load Group Details
async function loadGroup() {
    try {
        const group = await API.get(`/groups/${groupId}`);
        document.getElementById('group-name').textContent = group.name;

        await loadMembers();
        await loadExpenses();
    } catch (error) {
        showToast(error.message, 'error');
        setTimeout(() => window.location.href = 'dashboard.html', 2000);
    }
}

// Load Members
async function loadMembers() {
    const list = document.getElementById('members-list');
    const select = document.getElementById('paid-by-select');

    try {
        const members = await API.get(`/groups/${groupId}/members`);
        currentMembers = members;

        list.innerHTML = members.map(m => `
            <div style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 500;">${m.user_name || 'User #' + m.user_id}</div>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">${m.role}</div>
                </div>
            </div>
        `).join('');

        // Update select for expenses
        select.innerHTML = members.map(m => `
            <option value="${m.user_id}">${m.user_name || 'User #' + m.user_id}</option>
        `).join('');

    } catch (error) {
        console.error('Error loading members:', error);
    }
}

// Load Expenses
async function loadExpenses() {
    const list = document.getElementById('expenses-list');

    try {
        const expenses = await API.get(`/groups/${groupId}/expenses/`);

        if (expenses.length === 0) {
            list.innerHTML = '<p class="text-muted">No hay gastos registrados</p>';
            return;
        }

        list.innerHTML = expenses.map(e => `
            <div style="padding: 1rem; background: var(--bg-color); border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid var(--border-color);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-weight: 600;">${e.title}</span>
                    <span style="color: var(--success-color); font-weight: 700;">$${e.amount_total}</span>
                </div>
                <div style="font-size: 0.875rem; color: var(--text-muted);">
                    Pagado por ${e.payer_name || 'User #' + e.paid_by}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

// Modals
const memberModal = document.getElementById('add-member-modal');
const expenseModal = document.getElementById('add-expense-modal');

function openAddMemberModal() { memberModal.classList.remove('hidden'); }
function closeAddMemberModal() { memberModal.classList.add('hidden'); }

function openAddExpenseModal() { expenseModal.classList.remove('hidden'); }
function closeAddExpenseModal() { expenseModal.classList.add('hidden'); }

// Forms
document.getElementById('add-member-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        user_id: parseInt(formData.get('user_id')),
        role: 'member'
    };

    try {
        await API.post(`/groups/${groupId}/members`, data);
        showToast('Miembro agregado', 'success');
        closeAddMemberModal();
        loadMembers();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

document.getElementById('add-expense-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    // Simple split: everyone involved equally
    const participants = currentMembers.map(m => ({
        user_id: m.user_id,
        amount_owed: parseFloat(formData.get('amount')) / currentMembers.length
    }));

    const data = {
        title: formData.get('description'),
        amount_total: parseFloat(formData.get('amount')),
        paid_by: parseInt(formData.get('paid_by_id')),
        participants: participants
    };

    try {
        await API.post(`/groups/${groupId}/expenses`, data);
        showToast('Gasto registrado', 'success');
        closeAddExpenseModal();
        loadExpenses();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Init
loadGroup();
