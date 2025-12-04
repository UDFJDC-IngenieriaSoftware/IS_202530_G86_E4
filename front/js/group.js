// Check auth
if (!API.token) {
    window.location.href = 'login.html';
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

        // Initialize participants when members are loaded
        updateParticipantsFields();

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
            <div class="expense-card" onclick="showExpenseDetails(${e.id})" style="padding: 1rem; background: var(--bg-color); border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid var(--border-color); cursor: pointer; transition: all 0.2s;">
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

// Show Expense Details
async function showExpenseDetails(expenseId) {
    const modal = document.getElementById('expense-details-modal');
    const content = document.getElementById('expense-details-content');

    content.innerHTML = '<p class="text-muted">Cargando detalles...</p>';
    modal.classList.remove('hidden');

    try {
        const expenses = await API.get(`/groups/${groupId}/expenses/`);
        const expense = expenses.find(e => e.id === expenseId);

        if (!expense) {
            content.innerHTML = '<p style="color: var(--error-color)">Gasto no encontrado</p>';
            return;
        }

        document.getElementById('expense-detail-title').textContent = expense.title;

        const date = expense.created_at ? new Date(expense.created_at).toLocaleString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }) : 'Fecha no disponible';

        content.innerHTML = `
            <div style="background: var(--bg-color); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                <div style="display: grid; gap: 1rem;">
                    <div>
                        <strong>Monto Total:</strong> 
                        <span style="color: var(--success-color); font-size: 1.25rem; font-weight: 700;">$${expense.amount_total.toFixed(2)}</span>
                    </div>
                    <div>
                        <strong>Creado por:</strong> ${expense.creator_name || 'Usuario #' + expense.created_by}
                    </div>
                    <div>
                        <strong>Pagado por:</strong> ${expense.payer_name || 'Usuario #' + expense.paid_by}
                    </div>
                    <div>
                        <strong>Fecha:</strong> ${date}
                    </div>
                </div>
            </div>

            <h4 style="margin-bottom: 1rem;">División del Gasto:</h4>
            <div style="background: var(--bg-color); padding: 1rem; border-radius: 0.5rem;">
                ${expense.participants.map(p => `
                    <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--card-bg); border-radius: 0.5rem; margin-bottom: 0.5rem;">
                        <span><strong>${p.participant_name || 'Usuario #' + p.user_id}</strong></span>
                        <span style="color: var(--success-color); font-weight: 600;">
                            $${p.amount_owed.toFixed(2)}
                            ${p.percentage ? ` (${p.percentage}%)` : ''}
                        </span>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        content.innerHTML = `<p style="color: var(--error-color)">Error: ${error.message}</p>`;
    }
}

function closeExpenseDetailsModal() {
    document.getElementById('expense-details-modal').classList.add('hidden');
}

// Modals
const memberModal = document.getElementById('add-member-modal');
const expenseModal = document.getElementById('add-expense-modal');
const balanceModal = document.getElementById('balance-modal');

function openAddMemberModal() { memberModal.classList.remove('hidden'); }
function closeAddMemberModal() { memberModal.classList.add('hidden'); }

function openAddExpenseModal() {
    updateParticipantsFields();
    expenseModal.classList.remove('hidden');
}
function closeAddExpenseModal() {
    expenseModal.classList.add('hidden');
    document.getElementById('add-expense-form').reset();
}

// Balance Modal
function openBalanceModal() {
    loadBalance();
    balanceModal.classList.remove('hidden');
}

function closeBalanceModal() {
    balanceModal.classList.add('hidden');
}

async function loadBalance() {
    const content = document.getElementById('balance-content');
    content.innerHTML = '<p class="text-muted">Cargando balance...</p>';

    try {
        const balance = await API.get(`/groups/${groupId}/balance`);

        if (balance.length === 0) {
            content.innerHTML = '<p class="text-muted">✅ Todas las cuentas están saldadas</p>';
            return;
        }

        // Get member names for display
        const memberMap = {};
        currentMembers.forEach(m => {
            memberMap[m.user_id] = m.user_name || `User #${m.user_id}`;
        });

        content.innerHTML = `
            <div style="background: var(--bg-color); padding: 1rem; border-radius: 0.5rem;">
                <h4 style="margin-bottom: 1rem;">Pagos Sugeridos:</h4>
                ${balance.map(b => `
                    <div style="padding: 0.75rem; background: var(--card-bg); border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid var(--primary-color);">
                        <strong>${memberMap[b.from]}</strong> debe pagar 
                        <span style="color: var(--success-color); font-weight: 700;">$${b.amount.toFixed(2)}</span> 
                        a <strong>${memberMap[b.to]}</strong>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        content.innerHTML = `<p style="color: var(--error-color)">Error: ${error.message}</p>`;
    }
}

// Split Method Handling
const splitMethodSelect = document.getElementById('split-method-select');
const participantsContainer = document.getElementById('participants-container');

splitMethodSelect.addEventListener('change', updateParticipantsFields);

function updateParticipantsFields() {
    const method = splitMethodSelect.value;
    const amount = parseFloat(document.getElementById('expense-amount').value) || 0;

    if (currentMembers.length === 0) {
        participantsContainer.innerHTML = '<p class="text-muted">Cargando miembros...</p>';
        return;
    }

    if (method === 'equal') {
        // Equal split - just show checkboxes
        participantsContainer.innerHTML = currentMembers.map(m => `
            <div style="display: flex; align-items: center; padding: 0.5rem 0;">
                <input type="checkbox" id="participant-${m.user_id}" value="${m.user_id}" checked style="margin-right: 0.5rem;">
                <label for="participant-${m.user_id}">${m.user_name || 'User #' + m.user_id}</label>
            </div>
        `).join('');
    } else if (method === 'percentage') {
        // Percentage split
        participantsContainer.innerHTML = `
            <div style="margin-bottom: 0.5rem;">
                ${currentMembers.map(m => `
                    <div style="display: grid; grid-template-columns: 1fr 100px; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
                        <label>${m.user_name || 'User #' + m.user_id}</label>
                        <div style="display: flex; align-items: center; gap: 0.25rem;">
                            <input type="number" class="form-input participant-percentage" data-user-id="${m.user_id}" 
                                   min="0" max="100" step="1" value="0" style="padding: 0.25rem;">
                            <span>%</span>
                        </div>
                    </div>
                `).join('')}
            </div>
            <small class="text-muted">Total: <span id="percentage-total">0</span>% (debe sumar 100%)</small>
        `;

        // Add listeners to update total
        document.querySelectorAll('.participant-percentage').forEach(input => {
            input.addEventListener('input', updatePercentageTotal);
        });
    } else if (method === 'manual') {
        // Manual split
        participantsContainer.innerHTML = `
            <div style="margin-bottom: 0.5rem;">
                ${currentMembers.map(m => `
                    <div style="display: grid; grid-template-columns: 1fr 120px; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
                        <label>${m.user_name || 'User #' + m.user_id}</label>
                        <input type="number" class="form-input participant-amount" data-user-id="${m.user_id}" 
                               min="0" step="0.01" value="0" style="padding: 0.25rem;">
                    </div>
                `).join('')}
            </div>
            <small class="text-muted">Total asignado: $<span id="amount-total">0.00</span> / $${amount.toFixed(2)}</small>
        `;

        // Add listeners to update total
        document.querySelectorAll('.participant-amount').forEach(input => {
            input.addEventListener('input', updateAmountTotal);
        });
    }
}

function updatePercentageTotal() {
    const inputs = document.querySelectorAll('.participant-percentage');
    let total = 0;
    inputs.forEach(input => {
        total += parseFloat(input.value) || 0;
    });
    document.getElementById('percentage-total').textContent = total.toFixed(0);
}

function updateAmountTotal() {
    const inputs = document.querySelectorAll('.participant-amount');
    let total = 0;
    inputs.forEach(input => {
        total += parseFloat(input.value) || 0;
    });
    document.getElementById('amount-total').textContent = total.toFixed(2);
}

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
    const splitMethod = formData.get('split_method');

    // Build participants array based on split method
    let participants = [];

    if (splitMethod === 'equal') {
        // Get checked participants
        const checkboxes = document.querySelectorAll('#participants-container input[type="checkbox"]:checked');
        participants = Array.from(checkboxes).map(cb => ({
            user_id: parseInt(cb.value)
        }));
    } else if (splitMethod === 'percentage') {
        // Get percentages
        const inputs = document.querySelectorAll('.participant-percentage');
        inputs.forEach(input => {
            const percentage = parseFloat(input.value) || 0;
            if (percentage > 0) {
                participants.push({
                    user_id: parseInt(input.dataset.userId),
                    percentage: percentage
                });
            }
        });
    } else if (splitMethod === 'manual') {
        // Get manual amounts
        const inputs = document.querySelectorAll('.participant-amount');
        inputs.forEach(input => {
            const amount = parseFloat(input.value) || 0;
            if (amount > 0) {
                participants.push({
                    user_id: parseInt(input.dataset.userId),
                    amount_owed: amount
                });
            }
        });
    }

    const data = {
        title: formData.get('description'),
        amount_total: parseFloat(formData.get('amount')),
        paid_by: parseInt(formData.get('paid_by_id')),
        split_method: splitMethod,
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

// Close modals on click outside
const expenseDetailsModal = document.getElementById('expense-details-modal');

memberModal.addEventListener('click', (e) => {
    if (e.target === memberModal) closeAddMemberModal();
});

expenseModal.addEventListener('click', (e) => {
    if (e.target === expenseModal) closeAddExpenseModal();
});

balanceModal.addEventListener('click', (e) => {
    if (e.target === balanceModal) closeBalanceModal();
});

expenseDetailsModal.addEventListener('click', (e) => {
    if (e.target === expenseDetailsModal) closeExpenseDetailsModal();
});

// Init
loadGroup();
