const API_BASE = "https://hrm-backend-al8a.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded, starting data fetch...");
    loadReportingEmployees(); 
    loadTasks();
});

// 1. Load Employees into BOTH dropdowns (Filter and Assignment)
async function loadReportingEmployees() {
    try {
        const response = await fetch(`${API_BASE}/employees`);
        if (!response.ok) throw new Error("Backend unreachable");
        const allEmployees = await response.json();

        // Check for the IDs in your HTML
        const assignmentDropdown = document.getElementById("assigned_to");
        const filterDropdown = document.getElementById("filterEmployee");

        const options = allEmployees.map(emp => 
            `<option value="${emp.id}">${emp.first_name} ${emp.last_name}</option>`
        ).join("");
        
        if (assignmentDropdown) {
            assignmentDropdown.innerHTML = `<option value="">Select Employee</option>` + options;
        } else {
            console.warn("HTML Error: Could not find id='assigned_to'");
        }

        if (filterDropdown) {
            filterDropdown.innerHTML = `<option value="">All Employees</option>` + options;
        } else {
            console.warn("HTML Error: Could not find id='filterEmployee'");
        }
    } catch (error) {
        console.error("Error loading employees:", error);
    }
}

// 2. Load Tasks and Statistics
async function loadTasks() {
    // Check if filter elements exist, otherwise use empty string
    const status = document.getElementById("filterStatus")?.value || "";
    const empId = document.getElementById("filterEmployee")?.value || "";

    // Bypass login check for now: Force Admin view to ensure data visibility
    const url = `${API_BASE}/get_dashboard_tasks?user_id=1&role=Admin&status=${status}&employee_id=${empId}`;
    
    try {
        const response = await fetch(url);
        const result = await response.json();

        // 1. Update Stats boxes
        const totalBox = document.getElementById("stat-total");
        const pendingBox = document.getElementById("stat-pending");
        const completedBox = document.getElementById("stat-completed");

        if (totalBox) totalBox.innerText = result.statistics.total;
        if (pendingBox) pendingBox.innerText = result.statistics.pending;
        if (completedBox) completedBox.innerText = result.statistics.completed;

        // 2. Update the Table
        const tableBody = document.getElementById("taskTableBody");
        if (tableBody) {
            if (result.tasks.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="7" class="text-center">No tasks found.</td></tr>`;
            } else {
                tableBody.innerHTML = result.tasks.map((task, index) => `
                    <tr>
                        <td>${index + 1}</td>
                        <td><span class="badge bg-light text-dark border">${task.employee_name}</span></td>
                        <td>${task.task_title}</td>
                        <td>${task.start_date}</td>
                        <td>${task.end_date}</td>
                        <td><span class="badge ${task.status === 'Completed' ? 'bg-success' : 'bg-warning'}">${task.status}</span></td>
                        <td>
                            <button class="btn btn-sm btn-outline-danger" onclick="confirmDelete(${task.task_id})">Delete</button>
                        </td>
                    </tr>
                `).join("");
            }
        } else {
            console.error("HTML Error: Could not find id='taskTableBody'");
        }
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
}

// 3. Create Task Function
async function handleTaskSubmit(event) {
    event.preventDefault();
    
    const data = {
        task_title: document.getElementById("task_title").value,
        task_description: document.getElementById("task_description").value,
        task_priority: document.getElementById("task_priority").value,
        employee_id: document.getElementById("assigned_to").value,
        assigned_by: 1, // Hardcoded for now
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
        location.reload(); // Refresh to show new data
    }
}

// 4. Delete Function
function confirmDelete(id) {
    if (confirm("Delete this task?")) {
        fetch(`${API_BASE}/delete_task/${id}`, { method: "DELETE" })
            .then(() => loadTasks());
    }
}