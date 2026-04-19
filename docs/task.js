const API_BASE = "https://hrm-backend-al8a.onrender.com";
let currentPage = 1;

document.addEventListener("DOMContentLoaded", () => {
    loadReportingEmployees(); 
    loadTasks();
});

// 1. Logic: Dropdowns for Task Assignment & Filters
async function loadReportingEmployees() {
    // Note: Ensure your login script saves user as: localStorage.setItem("user", JSON.stringify(data))
    const userStr = localStorage.getItem("user");
    if (!userStr) return;
    
    const loggedInUser = JSON.parse(userStr); 
    const response = await fetch(`${API_BASE}/employees`);
    const allEmployees = await response.json();

    // Show all for Admin, only direct reports for Managers
    const filtered = allEmployees.filter(emp => 
        loggedInUser.role === 'Admin' || emp.reporting_manager_id === loggedInUser.id
    );

    const dropdown = document.getElementById("assigned_to");
    const filterDropdown = document.getElementById("filterEmployee");

    const options = filtered.map(emp => `<option value="${emp.id}">${emp.first_name} ${emp.last_name}</option>`).join("");
    
    if(dropdown) dropdown.innerHTML = `<option value="">Select Employee</option>` + options;
    if(filterDropdown) filterDropdown.innerHTML = `<option value="">All Employees</option>` + options;
}

// 2. Logic: Load tasks with styling
async function loadTasks(page = 1) {
    currentPage = page;
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) return;

    const status = document.getElementById("filterStatus").value;
    const empId = document.getElementById("filterEmployee").value;

    const url = `${API_BASE}/get_dashboard_tasks?user_id=${user.id}&role=${user.role}&status=${status}&employee_id=${empId}&page=${page}`;
    
    try {
        const response = await fetch(url);
        const result = await response.json();

        // Update Statistics (The Bars)
        document.getElementById("stat-total").innerText = result.statistics.total;
        document.getElementById("stat-pending").innerText = result.statistics.pending;
        document.getElementById("stat-completed").innerText = result.statistics.completed;

        // Helper for Status Badge Styling
        const getStatusBadge = (status) => {
            if (status === 'Completed') return 'bg-success';
            if (status === 'Pending') return 'bg-danger text-white';
            return 'bg-warning text-dark';
        };

        // Update Table
        const tableBody = document.getElementById("taskTableBody");
        tableBody.innerHTML = result.tasks.map((task, index) => `
            <tr>
                <td class="fw-bold text-muted">${(page - 1) * 10 + (index + 1)}</td>
                <td><span class="badge bg-light text-dark border p-2">${task.employee_name}</span></td>
                <td class="fw-semibold">${task.task_title}</td>
                <td class="small text-muted">${task.start_date}</td>
                <td class="small text-muted">${task.end_date}</td>
                <td><span class="badge ${getStatusBadge(task.status)}">${task.status}</span></td>
                <td class="text-center">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editTask(${task.task_id})">Edit</button>
                        <button class="btn btn-outline-danger" onclick="confirmDelete(${task.task_id})">Delete</button>
                    </div>
                </td>
            </tr>
        `).join("");
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
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
        alert("Task Created Successfully!");
        closeTaskModal();
        loadTasks();
        e.target.reset(); // Clear the form
    }
});

// Delete Logic
function confirmDelete(id) {
    if (confirm("Are you sure you want to delete this task?")) {
        fetch(`${API_BASE}/delete_task/${id}`, { method: "DELETE" })
            .then(() => loadTasks());
    }
}

// Modal Toggle Functions
function openTaskModal() { 
    document.getElementById("taskModal").style.display = "block"; 
    if(document.getElementById("modalOverlay")) document.getElementById("modalOverlay").style.display = "block";
}

function closeTaskModal() { 
    document.getElementById("taskModal").style.display = "none"; 
    if(document.getElementById("modalOverlay")) document.getElementById("modalOverlay").style.display = "none";
}