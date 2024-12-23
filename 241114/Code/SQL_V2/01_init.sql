-- �������ݿ�
CREATE DATABASE SDDB;
GO

-- ʹ�����ݿ�
USE SDDB;
GO

-- �����û���1
CREATE TABLE users (
    uuid UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(), -- �û�ȫ��Ψһ��ʶ
    username VARCHAR(50) NOT NULL UNIQUE,             -- �û���
    password VARCHAR(100) NOT NULL,                   -- �������루�����׶Σ�
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'doctor', 'patient', 'worker')), -- �û���ɫ����
    role_id INT NULL                                  -- ��ɫ������ ID����Ϊ���
);
GO

-- �������߱�1
CREATE TABLE patients (
    patient_id INT PRIMARY KEY IDENTITY(10000001, 1), -- ���� ID��8 λ���֣��Զ�����
    name VARCHAR(50) NULL,                            -- ��������
    gender VARCHAR(10) NULL CHECK (gender IN ('��', 'Ů')), -- �Ա�
    age INT NULL,                                     -- ����
    contact_number VARCHAR(15) NULL                  -- ��ϵ��ʽ
);
GO
-- 1
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,                        -- ҽ�� ID����������
    name VARCHAR(50) NULL,                            -- ҽ������
    gender VARCHAR(10) NULL CHECK (gender IN ('��', 'Ů')), -- �Ա�
    department VARCHAR(50) NULL,                     -- ����
    title VARCHAR(50) NULL,                          -- ְ��
    contact_number VARCHAR(15) NULL                  -- ��ϵ��ʽ
);
GO

CREATE TABLE workers (
    worker_id INT PRIMARY KEY IDENTITY(10000001, 1),  -- ���� ID��8 λ���֣��Զ�����
    name VARCHAR(50) NULL,                            -- ��������
    age INT NULL,                                     -- ����
    contact_number VARCHAR(15) NULL                  -- ��ϵ��ʽ
);
GO

CREATE TABLE admins (
    admin_id INT PRIMARY KEY IDENTITY(1, 1),          -- ����Ա ID��4 λ���֣��Զ�����
    name VARCHAR(50) NULL,                            -- ����Ա����
    contact_number VARCHAR(15) NULL                  -- ��ϵ��ʽ
);
GO
-- 1
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY IDENTITY(1, 1),   -- ���� ID���Զ�����
    patient_id INT NULL FOREIGN KEY REFERENCES patients(patient_id), -- ��������
    doctor_id INT NULL FOREIGN KEY REFERENCES doctors(doctor_id),    -- ����ҽ��
    date DATETIME DEFAULT GETDATE() NOT NULL,         -- ����ʱ�䣬Ĭ�ϵ�ǰʱ��
    amount FLOAT NULL,                                -- �ܽ��
    usage_instructions TEXT NULL,                    -- ��ҩ˵��
    status VARCHAR(20) DEFAULT '���䷽' CHECK (status IN ('���䷽', '������', '����ҩ', '�����')), -- ����״̬
    expected_pickup_time DATETIME NULL               -- Ԥ��ȡҩʱ�䣨�������Զ����㣩
);
GO
-- 1
CREATE TABLE tasks (
    task_id INT PRIMARY KEY IDENTITY(1, 1),           -- ���� ID���Զ�����
    prescription_id INT NULL FOREIGN KEY REFERENCES prescriptions(prescription_id), -- ��������
    receive_worker_id INT NULL FOREIGN KEY REFERENCES workers(worker_id), -- �շ����� ID
    receive_worker_name VARCHAR(50) NULL,            -- �շ���������
    form_worker_id INT NULL FOREIGN KEY REFERENCES workers(worker_id), -- �䷽���� ID
    form_worker_name VARCHAR(50) NULL,               -- �䷽��������
    decoction_worker_id INT NULL FOREIGN KEY REFERENCES workers(worker_id), -- ��ҩ���� ID
    decoction_worker_name VARCHAR(50) NULL,          -- ��ҩ��������
    admin_id INT NULL FOREIGN KEY REFERENCES admins(admin_id), -- ����������Ա ID
    admin_name VARCHAR(50) NULL,                     -- ����������Ա����
    receive_time DATETIME NULL,                      -- ��������ʱ��
    form_time DATETIME NULL,                         -- �䷽ʱ��
    decoction_start_time DATETIME NULL,              -- ��ҩ��ʼʱ��
    decoction_end_time DATETIME NULL,                -- ��ҩ����ʱ��
    status VARCHAR(20) DEFAULT 'δ���' CHECK (status IN ('δ���', '���')) -- ����״̬
);
GO
