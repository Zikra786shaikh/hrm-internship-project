CREATE DATABASE hrm_system;

USE hrm_system;

CREATE TABLE department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100),
    description VARCHAR(300),
    created_at DATETIME,
    updated_at DATETIME,
    status BOOLEAN DEFAULT TRUE
);
