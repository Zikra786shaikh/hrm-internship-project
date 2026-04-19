-- =========================================
-- Employee Table (User Table)
-- =========================================
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(100),
    last_name VARCHAR(100),

    username VARCHAR(100) UNIQUE,
    password VARCHAR(100),

    email VARCHAR(100),
    mobile VARCHAR(15),

    dept_id INT,
    role_id INT,
    reporting_manager_id INT,

    date_of_joining DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    status INT DEFAULT 1,

    -- FOREIGN KEYS
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (reporting_manager_id) REFERENCES user(employee_id)
);


-- =========================================
-- Sample Data for Testing
-- =========================================

INSERT INTO user 
(first_name, last_name, username, password, email, mobile, dept_id, role_id, reporting_manager_id, date_of_joining)
VALUES

('Admin', 'User', 'admin', '1234', 'admin@gmail.com', '9999999999', 1, 1, NULL, '2024-01-01'),

('Rahul', 'Manager', 'manager', '1234', 'manager@gmail.com', '8888888888', 2, 2, 1, '2024-02-01'),

('Aisha', 'Khan', 'aisha', '1234', 'aisha@gmail.com', '7777777777', 2, 3, 2, '2024-03-01'),

('Zoya', 'Shaikh', 'zoya', '1234', 'zoya@gmail.com', '6666666666', 1, 3, 2, '2024-03-10');