CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(100) NOT NULL,
    role NVARCHAR(20) NOT NULL
);

-- 插入测试数据
INSERT INTO Users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('doctor', 'doctor123', 'doctor'),
('patient', 'patient123', 'patient');
