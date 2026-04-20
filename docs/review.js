const API_BASE = "https://hrm-backend-al8a.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
    loadReviewEmployees();
    loadReviewTable();
});

// Populate "Select Employee" dropdown with those reporting to user [cite: 8, 18]
async function loadReviewEmployees() {
    const response = await fetch(`${API_BASE}/employees`);
    const employees = await response.json();
    const dropdown = document.getElementById("review_employee_id");
    
    if (dropdown) {
        dropdown.innerHTML = '<option value="">Select Employee</option>' + 
            employees.map(emp => `<option value="${emp.id}">${emp.first_name} ${emp.last_name}</option>`).join("");
    }
}

// Submit the Review [cite: 17]
async function handleReviewSubmit(event) {
    event.preventDefault();
    const data = {
        review_title: document.getElementById("review_title").value,
        employee_id: document.getElementById("review_employee_id").value,
        reviewed_by: 1, // Assume Admin for now
        review_date: document.getElementById("review_date").value,
        review_period: document.getElementById("review_period").value,
        rating: document.getElementById("review_rating").value,
        comments: document.getElementById("review_comments").value
    };

    const res = await fetch(`${API_BASE}/add_review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Review Saved!");
        location.reload();
    }
}

// Load Review Dashboard Table [cite: 20]
async function loadReviewTable() {
    const res = await fetch(`${API_BASE}/get_reviews`);
    const data = await res.json();
    
    // Update Stats Boxes 
    const monthly = data.filter(r => r.review_period === 'Monthly').length;
    const quarterly = data.filter(r => r.review_period === 'Quarterly').length;
    const annual = data.filter(r => r.review_period === 'Annual').length;

    if(document.getElementById("stat-monthly")) document.getElementById("stat-monthly").innerText = monthly;
    if(document.getElementById("stat-quarterly")) document.getElementById("stat-quarterly").innerText = quarterly;
    if(document.getElementById("stat-annual")) document.getElementById("stat-annual").innerText = annual;

    // Update Table [cite: 26, 29, 30, 33, 34]
    const tableBody = document.getElementById("reviewTableBody");
    if (tableBody) {
        tableBody.innerHTML = data.map((r, i) => `
            <tr>
                <td>${i + 1}</td>
                <td>${r.employee_name}</td>
                <td>${r.review_title}</td>
                <td>${r.review_date}</td>
                <td>${r.review_period}</td>
                <td><span class="badge bg-primary">${r.rating}/10</span></td>
               <td><button class="btn btn-sm btn-info text-white" onclick="viewComments(${r.review_id})">View</button></td>
            </tr>
        `).join("");
    }
    async function viewComments(id) {
    try {
        const res = await fetch(`${API_BASE}/get_reviews`);
        const reviews = await res.json();
        
        // Find the specific review by ID
        const review = reviews.find(r => r.review_id === id);
        
        if (review) {
            alert(`Review Comments for ${review.employee_name}:\n\n"${review.comments}"`);
        } else {
            alert("Review not found.");
        }
    } catch (error) {
        console.error("Error fetching comments:", error);
    }
}
}