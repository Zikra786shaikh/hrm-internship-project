const API_BASE = "https://hrm-backend-al8a.onrender.com"; // Replace with your Render URL
let currentPage = 1;

// Load initial data
document.addEventListener("DOMContentLoaded", () => {
    loadReportingEmployees(); 
    loadTasks();
});

// 1. Logic: Show only employees reporting to the logged-in user
async function loadReportingEmployees() {
    const loggedInUser = JSON.parse(localStorage.getItem("user")); // Assuming you store user data on login
    const response = await fetch(`${API_BASE}/employees`);
    const allEmployees = await response.json();

    // Filter: Show all for Admin, only direct reports for Managers
    const filtered = allEmployees.filter(emp => 
        loggedInUser.role === 'Admin' || emp.reporting_manager_id === loggedInUser.id
    );

    const dropdown = document.getElementById("assigned_to");
    const filterDropdown = document.getElementById("filterEmployee");

    const options = filtered.map(emp => `<option value="${emp.id}">${emp.first_name} ${emp.last_name}</option>`).join("");
    dropdown.innerHTML = `<option value="">Select Employee</option>` + options;
    filterDropdown.innerHTML = `<option value="">All Employees</option>` + options;
}

// 2. Logic: Load tasks with filters and pagination
async function loadTasks(page = 1) {
    currentPage = page;
    const user = JSON.parse(localStorage.getItem("user"));
    const status = document.getElementById("filterStatus").value;
    const empId = document.getElementById("filterEmployee").value;

    const url = `${API_BASE}/get_dashboard_tasks?user_id=${user.id}&role=${user.role}&status=${status}&employee_id=${empId}&page=${page}`;
    
    const response = await fetch(url);
    const result = await response.json();

    // Update Stats
    document.getElementById("stat-total").innerText = result.statistics.total;
    document.getElementById("stat-pending").innerText = result.statistics.pending;
    document.getElementById("stat-progress").innerText = result.statistics.in_progress;
    document.getElementById("stat-completed").innerText = result.statistics.completed;

    // Update Table
    const tableBody = document.getElementById("taskTableBody");
    tableBody.innerHTML = result.tasks.map((task, index) => `
        <tr>
            <td>${(page - 1) * 10 + (index + 1)}</td>
            <td>${task.employee_name}</td>
            <td>${task.task_title}</td>
            <td>${task.start_date}</td>
            <td>${task.end_date}</td>
            <td>${task.status}</td>
            <td>
                <button onclick="editTask(${task.task_id})">Edit</button>
                <button onclick="confirmDelete(${task.task_id})">Delete</button>
            </td>
        </tr>
    `).join("");
}

// 3. Logic: Create Task
document.getElementById("taskForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user = JSON.parse(localStorage.getItem("user"));

    const data = {
        task_title: document.getElementById("task_title").value,
        task_description: document.getElementById("task_description").value,
        task_priority: document.getElementById("task_priority").value,
        employee_id: parseInt(document.getElementById("assigned_to").value),
        assigned_by: user.id,
        start_date: document.getElementById("start_date").value,
        end_date: document.getElementById("end_date").value,
        task_type: document.getElementById("task_type").value
    };

    const response = await fetch(`${API_BASE}/add_task`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert("Task Created!");
        closeTaskModal();
        loadTasks();
    }
});

function confirmDelete(id) {
    if (confirm("Are you sure you want to delete this task?")) {
        fetch(`${API_BASE}/delete_task/${id}`, { method: "DELETE" })
            .then(() => loadTasks());
    }
}

// Modal Toggle Functions
function openTaskModal() { document.getElementById("taskModal").style.display = "block"; }
function closeTaskModal() { document.getElementById("taskModal").style.display = "none"; }