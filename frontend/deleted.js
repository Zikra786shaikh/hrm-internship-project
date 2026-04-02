const API = "http://127.0.0.1:5000"; // 🔴 CHANGE AFTER DEPLOY

window.onload = function () {
    loadDeleted();
};

async function loadDeleted() {

    let res = await fetch(`${API}/deleted_departments`);
    let data = await res.json();

    let table = document.getElementById("deletedTable");
    table.innerHTML = "";

    data.forEach(dept => {
        table.innerHTML += `
            <tr>
                <td>${dept.dept_id}</td>
                <td>${dept.dept_name}</td>
                <td>${dept.description}</ td>
                <td>
                    <button onclick="restore(${dept.dept_id})">Restore</button>
                </td>
            </tr>
        `;
    });
}

async function restore(id) {

    await fetch(`${API}/restore_department/${id}`, {
        method: "PUT"
    });

    alert("Restored!");
    loadDeleted();
}