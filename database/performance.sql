-- 1. Create the Database (if not already created)
CREATE DATABASE IF NOT EXISTS hrm_system;
USE hrm_system;

-- 2. Performance Review Table Structure
-- Based on project requirements for Rating (1-10) and Review Periods
CREATE TABLE IF NOT EXISTS performance_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    review_title VARCHAR(100) NOT NULL,
    review_date DATE NOT NULL,
    employee_id INT NOT NULL,
    reviewed_by INT NOT NULL,
    review_period ENUM('Monthly', 'Quarterly', 'Annual') NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 10),
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Relationships (Assuming you have an employees table)
    CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    CONSTRAINT fk_reviewer FOREIGN KEY (reviewed_by) REFERENCES employees(id) ON DELETE CASCADE
);

-- 3. Dummy Data for Testing
-- These match the "John Doe" and "Jane Smith" records we used in Python
INSERT INTO performance_reviews (review_title, review_date, employee_id, reviewed_by, review_period, rating, comments)
VALUES 
('Quarterly Performance Sync', '2026-03-15', 2, 1, 'Quarterly', 9, 'Excellent progress on database design and backend architecture.'),
('Monthly Progress Check', '2026-04-01', 3, 1, 'Monthly', 8, 'Great work on API integration. Needs to focus more on security audits.'),
('Annual Excellence Review', '2026-01-10', 2, 1, 'Annual', 10, 'Consistently top performer. Promoted to Senior Developer role.');