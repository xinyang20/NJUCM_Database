-- 删除旧的 Users 表（如果存在）
DROP TABLE IF EXISTS Users;

-- 创建新的 Users 表
CREATE TABLE Users (
    account_id INT PRIMARY KEY IDENTITY(1,1),  -- 自动递增的账号 ID
    username NVARCHAR(50) UNIQUE NOT NULL,    -- 用户名
    password NVARCHAR(100) NOT NULL,          -- 密码
    role NVARCHAR(50) NOT NULL,               -- 用户角色（admin、doctor、patient）
    related_id INT NULL                       -- 关联医生或患者表的 ID，可为空
);

-- 插入示例数据
INSERT INTO Users (username, password, role, related_id)
VALUES
    ('admin', 'admin123', 'admin', NULL),      -- 管理员无需关联
    ('doctor1', 'doctor123', 'doctor', 1),    -- 关联医生表中的 ID 为 1
    ('patient1', 'patient123', 'patient', 2); -- 关联患者表中的 ID 为 2
