-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS hrm_leave_system;
USE hrm_leave_system;

-- 2. Create Leave Quota Table
CREATE TABLE leave_quota (
    quotaid INT AUTO_INCREMENT PRIMARY KEY,
    employeeid INT NOT NULL,
    leave_type ENUM('SL', 'CL', 'PL') NOT NULL,
    total_quota INT NOT NULL,
    used_quota INT DEFAULT 0,
    remain_quota INT AS (total_quota - used_quota),
    FOREIGN KEY (employeeid) REFERENCES employees(id)
);

-- 3. Create Leave Requests Table
CREATE TABLE leave_requests (
    leaveid INT AUTO_INCREMENT PRIMARY KEY,
    employeeid INT NOT NULL,
    leave_type ENUM('SL', 'CL', 'PL') NOT NULL,
    reason VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeid) REFERENCES employees(id)
);

-- 4. Insert Raw Data for Understanding (Testing)
-- Quotas for John Doe (ID 2)
INSERT INTO leave_quota (employeeid, leave_type, total_quota, used_quota) VALUES 
(2, 'SL', 7, 1),
(2, 'CL', 3, 0),
(2, 'PL', 10, 2);

-- Quotas for Jane Smith (ID 3)
INSERT INTO leave_quota (employeeid, leave_type, total_quota, used_quota) VALUES 
(3, 'SL', 7, 0),
(3, 'CL', 3, 0),
(3, 'PL', 10, 0);

-- Existing Leave Records
INSERT INTO leave_requests (employeeid, leave_type, reason, start_date, end_date, status) VALUES 
(2, 'PL', 'Personal family function in hometown', '2026-03-01', '2026-03-03', 'approved'),
(2, 'SL', 'Severe viral fever', '2026-04-10', '2026-04-11', 'approved'),
(3, 'CL', 'Out of town for urgent work', '2026-04-20', '2026-04-22', 'pending'),
(2, 'PL', 'Summer Vacation', '2026-05-15', '2026-05-20', 'rejected');