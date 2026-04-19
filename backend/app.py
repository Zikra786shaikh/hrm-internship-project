// Replace the login fetch block in index.html
let response = await fetch(`${API}/admin_login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password })
});

let data = await response.json();

if (response.status === 200) {
    localStorage.setItem("role", data.role);
    localStorage.setItem("user_id", data.id); // Save ID for task filtering
    document.getElementById("message").innerText = "Login success";
    setTimeout(() => { window.location.href = "dashboard.html"; }, 800);
} else {
    document.getElementById("message").innerText = "Invalid login";
}