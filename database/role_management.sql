-- CREATE ROLE TABLE
CREATE TABLE role (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL,
    permissions TEXT,
    department_id INT,
    status INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INSERT SAMPLE DATA
INSERT INTO role (role_name, permissions, department_id, status)
VALUES 
('Admin', 'add,edit,delete', 1, 1),
('Manager', 'add,view', 1, 1),
('Employee', 'view', 2, 1);

-- SELECT ACTIVE ROLES
SELECT * FROM role WHERE status = 1;

-- SOFT DELETE
UPDATE role SET status = 0 WHERE role_id = 1;

-- RESTORE ROLE
UPDATE role SET status = 1 WHERE role_id = 1;

-- UPDATE ROLE
UPDATE role 
SET role_name = 'HR Manager', permissions = 'add,edit'
WHERE role_id = 2;