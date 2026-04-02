const API = "https://hrm-backend-al8a.onrender.com"; // 🔴 CHANGE AFTER DEPLOY

// Load departments
window.onload = function () {
    fetchDepartments();
};

// Fetch departments
async function fetchDepartments() {

    let response = await fetch(`${API}/departments`);
    let data = await response.json();

    let table = document.getElementById("deptTable");
    table.innerHTML = "";

    data.forEach(dept => {
        table.innerHTML += `
            <tr>
                <td>${dept.dept_id}</td>
                <td>${dept.dept_name}</td>
                <td>${dept.description}</td>
                <td>
                    <button onclick="editDepartment(${dept.dept_id}, '${dept.dept_name}', '${dept.description}')" class="btn btn-warning btn-sm">Edit</button>
                    <button onclick="deleteDepartment(${dept.dept_id})" class="btn btn-danger btn-sm">Delete</button>
                </td>
            </tr>
        `;
    });
}


// Add
async function addDepartment() {

    let dept_name = document.getElementById("dept_name").value;
    let description = document.getElementById("description").value;

    await fetch(`${API}/add_department`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ dept_name, description })
    });

    fetchDepartments();
}


// Delete
async function deleteDepartment(id) {

    let confirmDelete = confirm("Are you sure?");
    if (!confirmDelete) return;

    let response = await fetch(`${API}/delete_department/${id}`, {
        method: "DELETE"
    });

    let data = await response.json();

    alert(data.message);
    fetchDepartments();
}


// Restore
async function restoreDepartment(id) {

    await fetch(`${API}/restore_department/${id}`, {
        method: "PUT"
    });

    alert("Restored");
    fetchDepartments();
}


// Edit
function editDepartment(id, name, desc) {

    let newName = prompt("Enter new name:", name);
    let newDesc = prompt("Enter new description:", desc);

    if (!newName || !newDesc) {
        alert("Cancelled");
        return;
    }

    fetch(`${API}/update_department/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            dept_name: newName,
            description: newDesc
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        fetchDepartments();
    });
}


// Logout
function logout() {
    localStorage.removeItem("adminLoggedIn");
    window.location.href = "login.html";
}
let response = await fetch(`${API}/admin_login`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
});

let text = await response.text();   // 👈 first get raw response
console.log("RAW:", text);

let data;

try {
    data = JSON.parse(text);
} catch {
    alert("Server error (not JSON)");
    return;
}