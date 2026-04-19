-- Create Task Table
CREATE TABLE task (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    task_title VARCHAR(100) NOT NULL,
    task_description VARCHAR(300),
    task_priority VARCHAR(50) CHECK (task_priority IN ('High', 'Medium', 'Low')) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    task_type VARCHAR(50) CHECK (task_type IN ('Individual', 'Team')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Task Assignment Table
CREATE TABLE task_assignment (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    employee_id INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) CHECK (status IN ('Pending', 'In Progress', 'Completed')) DEFAULT 'Pending',
    completed_at DATETIME NULL,

    -- Foreign Keys
    CONSTRAINT fk_task FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE CASCADE,
    CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES user(employee_id) ON DELETE CASCADE,
    CONSTRAINT fk_assigned_by FOREIGN KEY (assigned_by) REFERENCES user(employee_id) ON DELETE CASCADE
);

-- Indexes for better performance (important for dashboard filters)
CREATE INDEX idx_task_priority ON task(task_priority);
CREATE INDEX idx_task_dates ON task(start_date, end_date);

CREATE INDEX idx_assignment_employee ON task_assignment(employee_id);
CREATE INDEX idx_assignment_status ON task_assignment(status);
CREATE INDEX idx_assignment_task ON task_assignment(task_id);