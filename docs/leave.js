const API_BASE = "https://hrm-backend-al8a.onrender.com";

document.addEventListener("DOMContentLoaded", loadLeaveData);

async function loadLeaveData() {
    // For demo, we use ID 2 (John Doe)
    const empId = 2; 
    const res = await fetch(`${API_BASE}/get_user_leaves/${empId}`);
    const data = await res.json();

    // Update Quota Displays
    document.getElementById("q-PL").innerText = data.quota.PL;
    document.getElementById("q-CL").innerText = data.quota.CL;
    document.getElementById("q-SL").innerText = data.quota.SL;

    // Update Table
    const tableBody = document.getElementById("leaveTableBody");
    tableBody.innerHTML = data.leaves.map((l, i) => {
    let badgeClass = "bg-warning"; // Default Pending
    if (l.status === 'approved') badgeClass = "bg-success";
    if (l.status === 'rejected') badgeClass = "bg-danger";

    return `
        <tr>
            <td>${i + 1}</td>
            <td>${l.reason}</td>
            <td><span class="badge border text-dark">${l.leave_type}</span></td>
            <td>${l.start_date}</td>
            <td>${l.end_date}</td>
            <td><span class="badge ${badgeClass}">${l.status.toUpperCase()}</span></td>
        </tr>
    `;
}).join("");
}

async function handleLeaveSubmit(event) {
    event.preventDefault();
    const data = {
        employeeid: 2, // Hardcoded for demo
        leave_type: document.getElementById("leave_type").value,
        reason: document.getElementById("leave_reason").value,
        start_date: document.getElementById("leave_from").value,
        end_date: document.getElementById("leave_to").value
    };

    const res = await fetch(`${API_BASE}/apply_leave`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Leave Applied!");
        location.reload();
    }
}