const API_URL = "http://localhost:8000";

//---------UTILIDADES--------------------------------------------------

function getTokin() {
    return localStroage.getItem("token");
}

function saveToken(token) {
    localStrorage.setItem("token", token);
}

function showError(msg) {
    const el = document.getElementById("error-msg");
    el.textContent = msg;
    el.style.display = "block";
}

function hideError() {
    const el = document.getElementById("error-msg");
    el.style.display = "none";
}


// ─── TABS ───────────────────────────────────────────────

function showTab(tab) {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const tabs = document.querySelectorAll(".tab");

    if (tab === "login") {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        tabs[0].classList.add("active");
        tabs[1].classList.remove("active");
    } else {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
        tabs[0].classList.remove("active");
        tabs[1].classList.add("active");
    }

    hideError();
}


// ─── AUTENTICACIÓN ──────────────────────────────────────

async function login() {
    hideError();

    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    if (!username || !password) {
        showError("Completá todos los campos");
        return;
    }

    // El login usa FormData porque el backend usa OAuth2PasswordRequestForm
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/users/login`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.detail || "Error al iniciar sesión");
            return;
        }

        saveToken(data.access_token);
        window.location.href = "dashboard.html";

    } catch (error) {
        showError("No se pudo conectar con el servidor");
    }
}


async function register() {
    hideError();

    const email = document.getElementById("register-email").value;
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    if (!email || !username || !password) {
        showError("Completá todos los campos");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.detail || "Error al registrarse");
            return;
        }

        // Registro exitoso → mostramos el login
        showTab("login");
        showError("¡Registro exitoso! Iniciá sesión.");
        document.getElementById("error-msg").style.backgroundColor = "#d1fae5";
        document.getElementById("error-msg").style.color = "#065f46";

    } catch (error) {
        showError("No se pudo conectar con el servidor");
    }
}


function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}


// ─── TAREAS ─────────────────────────────────────────────

async function loadTasks() {
    const token = getToken();

    if (!token) {
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (response.status === 401) {
            logout();
            return;
        }

        const tasks = await response.json();
        renderTasks(tasks);

    } catch (error) {
        showError("No se pudo cargar las tareas");
    }
}


function renderTasks(tasks) {
    const list = document.getElementById("tasks-list");

    if (tasks.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <p>No tenés tareas todavía. ¡Creá una!</p>
            </div>
        `;
        return;
    }

    list.innerHTML = tasks.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}">
            <input 
                type="checkbox" 
                ${task.completed ? 'checked' : ''}
                onchange="toggleTask(${task.id}, ${task.completed})"
            >
            <div class="task-info">
                <h3 class="${task.completed ? 'completed-text' : ''}">${task.title}</h3>
                ${task.description ? `<p>${task.description}</p>` : ''}
            </div>
            <button class="btn btn-danger" onclick="deleteTask(${task.id})">Eliminar</button>
        </div>
    `).join('');
}


async function createTask() {
    hideError();

    const title = document.getElementById("task-title").value;
    const description = document.getElementById("task-description").value;
    const token = getToken();

    if (!title) {
        showError("El título es obligatorio");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ title, description })
        });

        if (!response.ok) {
            showError("Error al crear la tarea");
            return;
        }

        // Limpiamos los inputs y recargamos las tareas
        document.getElementById("task-title").value = "";
        document.getElementById("task-description").value = "";
        loadTasks();

    } catch (error) {
        showError("No se pudo conectar con el servidor");
    }
}


async function toggleTask(taskId, currentCompleted) {
    const token = getToken();

    try {
        await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ completed: !currentCompleted })
        });

        loadTasks();

    } catch (error) {
        showError("Error al actualizar la tarea");
    }
}


async function deleteTask(taskId) {
    const token = getToken();

    try {
        await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        loadTasks();

    } catch (error) {
        showError("Error al eliminar la tarea");
    }
}


// ─── INICIO ─────────────────────────────────────────────

// Si estamos en el dashboard, cargamos las tareas automáticamente
if (document.getElementById("tasks-list")) {
    loadTasks();
}