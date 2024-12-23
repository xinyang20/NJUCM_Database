-- 创建数据库
CREATE DATABASE SDDB;
GO

-- 使用数据库
USE SDDB;
GO

-- 创建用户表1
CREATE TABLE users (
    uuid UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(), -- 用户全局唯一标识
    username VARCHAR(50) NOT NULL UNIQUE,             -- 用户名
    password VARCHAR(100) NOT NULL,                   -- 明文密码（开发阶段）
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'doctor', 'patient', 'worker')), -- 用户角色类型
    role_id INT NULL                                  -- 角色表主键 ID，作为外键
);
GO

-- 创建患者表1
CREATE TABLE patients (
    patient_id INT PRIMARY KEY IDENTITY(10000001, 1), -- 患者 ID，8 位数字，自动生成
    name VARCHAR(50) NULL,                            -- 患者姓名
    gender VARCHAR(10) NULL CHECK (gender IN ('男', '女')), -- 性别
    age INT NULL,                                     -- 年龄
    contact_number VARCHAR(15) NULL                  -- 联系方式
);
GO
-- 1
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,                        -- 医生 ID，规则生成
    name VARCHAR(50) NULL,                            -- 医生姓名
    gender VARCHAR(10) NULL CHECK (gender IN ('男', '女')), -- 性别
    department VARCHAR(50) NULL,                     -- 科室
    title VARCHAR(50) NULL,                          -- 职称
    contact_number VARCHAR(15) NULL                  -- 联系方式
);
GO

CREATE TABLE workers (
    worker_id INT PRIMARY KEY IDENTITY(10000001, 1),  -- 工人 ID，8 位数字，自动生成
    name VARCHAR(50) NULL,                            -- 工人姓名
    age INT NULL,                                     -- 年龄
    contact_number VARCHAR(15) NULL                  -- 联系方式
);
GO

CREATE TABLE admins (
    admin_id INT PRIMARY KEY IDENTITY(1, 1),          -- 管理员 ID，4 位数字，自动生成
    name VARCHAR(50) NULL,                            -- 管理员姓名
    contact_number VARCHAR(15) NULL                  -- 联系方式
);
GO
-- 1
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY IDENTITY(1, 1),   -- 处方 ID，自动生成
    patient_id INT NULL FOREIGN KEY REFERENCES patients(patient_id), -- 关联患者
    doctor_id INT NULL FOREIGN KEY REFERENCES doctors(doctor_id),    -- 关联医生
    date DATETIME DEFAULT GETDATE() NOT NULL,         -- 开方时间，默认当前时间
    amount FLOAT NULL,                                -- 总金额
    usage_instructions TEXT NULL,                    -- 用药说明
    status VARCHAR(20) DEFAULT '待配方' CHECK (status IN ('待配方', '待浸泡', '待煎药', '已完成')), -- 处方状态
    expected_pickup_time DATETIME NULL               -- 预计取药时间（触发器自动计算）
);
GO
-- 1
CREATE TABLE tasks (
    task_id INT PRIMARY KEY IDENTITY(1, 1),           -- 任务 ID，自动生成
    prescription_id INT NULL FOREIGN KEY REFERENCES prescriptions(prescription_id), -- 关联处方
    receive_worker_id INT NULL FOREIGN KEY REFERENCES workers(worker_id), -- 收方工人 ID
    receive_worker_name VARCHAR(50) NULL,            -- 收方工人姓名
    form_worker_id INT NULL FOREIGN KEY REFERENCES workers(worker_id), -- 配方工人 ID
    form_worker_name VARCHAR(50) NULL,               -- 配方工人姓名
    decoction_worker_id INT NULL FOREIGN KEY REFERENCES workers(worker_id), -- 煎药工人 ID
    decoction_worker_name VARCHAR(50) NULL,          -- 煎药工人姓名
    admin_id INT NULL FOREIGN KEY REFERENCES admins(admin_id), -- 任务分配管理员 ID
    admin_name VARCHAR(50) NULL,                     -- 任务分配管理员姓名
    receive_time DATETIME NULL,                      -- 处方接收时间
    form_time DATETIME NULL,                         -- 配方时间
    decoction_start_time DATETIME NULL,              -- 煎药开始时间
    decoction_end_time DATETIME NULL,                -- 煎药结束时间
    status VARCHAR(20) DEFAULT '未完成' CHECK (status IN ('未完成', '完成')) -- 任务状态
);
GO
