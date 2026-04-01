// Load departments when page opens
window.onload = function() {
    fetchDepartments();
};

// Fetch all departments
async function fetchDepartments() {

    let response = await fetch("http://127.0.0.1:5000/departments");
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

// Add department
async function addDepartment() {

    let dept_name = document.getElementById("dept_name").value;
    let description = document.getElementById("description").value;

    await fetch("http://127.0.0.1:5000/add_department", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ dept_name, description })
    });

    fetchDepartments();
}

// Delete department
async function deleteDepartment(id) {

    let confirmDelete = confirm("Are you sure you want to delete this department?");

    if (!confirmDelete) return;

    let response = await fetch(`http://127.0.0.1:5000/delete_department/${id}`, {
        method: "DELETE"
    });

    let data = await response.json();

    alert(data.message);

    fetchDepartments();

}
async function restoreDepartment(id) {

    await fetch(`http://127.0.0.1:5000/restore_department/${id}`, {
        method: "PUT"
    });

    alert("Department restored");
    fetchDepartments();
}

// Edit department
function editDepartment(id, name, desc) {

    let newName = prompt("Enter new name:", name);
    let newDesc = prompt("Enter new description:", desc);

    fetch(`http://127.0.0.1:5000/update_department/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            dept_name: newName,
            description: newDesc
        })
    }).then(() => fetchDepartments());
}