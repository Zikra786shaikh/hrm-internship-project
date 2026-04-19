-- =========================================
-- TABLE: otp_verification
-- Stores OTP for password reset
-- =========================================

CREATE TABLE otp_verification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    otp VARCHAR(10) NOT NULL,
    is_verified INT DEFAULT 0, -- 0 = not verified, 1 = verified
    status INT DEFAULT 1, -- 1 = active, 0 = deleted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =========================================
-- SAMPLE DATA: otp_verification
-- =========================================

INSERT INTO otp_verification (email, otp, is_verified) VALUES
('admin@gmail.com', '123456', 0),
('test@gmail.com', '654321', 1),
('user1@gmail.com', '987654', 0);


-- =========================================
-- TABLE: login_logs
-- Tracks login attempts (useful for reports)
-- =========================================

CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    username VARCHAR(50),
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20), -- success / failed
    ip_address VARCHAR(50),
    
    FOREIGN KEY (employee_id) REFERENCES user(employee_id)
);

-- =========================================
-- SAMPLE DATA: login_logs
-- =========================================

INSERT INTO login_logs (employee_id, username, status, ip_address) VALUES
(1, 'admin', 'success', '127.0.0.1'),
(1, 'admin', 'failed', '127.0.0.1'),
(NULL, 'unknown', 'failed', '192.168.1.10');


-- =========================================
-- OPTIONAL: password_reset_history
-- Tracks password changes (good for audit)
-- =========================================

CREATE TABLE password_reset_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    email VARCHAR(100),
    reset_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20), -- success / failed

    FOREIGN KEY (employee_id) REFERENCES user(employee_id)
);

-- =========================================
-- SAMPLE DATA: password_reset_history
-- =========================================

INSERT INTO password_reset_history (employee_id, email, status) VALUES
(1, 'admin@gmail.com', 'success'),
(1, 'admin@gmail.com', 'success'),
(NULL, 'test@gmail.com', 'failed');