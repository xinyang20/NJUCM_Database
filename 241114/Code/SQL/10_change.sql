-- ɾ���ɵ� Users ��������ڣ�
DROP TABLE IF EXISTS Users;

-- �����µ� Users ��
CREATE TABLE Users (
    account_id INT PRIMARY KEY IDENTITY(1,1),  -- �Զ��������˺� ID
    username NVARCHAR(50) UNIQUE NOT NULL,    -- �û���
    password NVARCHAR(100) NOT NULL,          -- ����
    role NVARCHAR(50) NOT NULL,               -- �û���ɫ��admin��doctor��patient��
    related_id INT NULL                       -- ����ҽ�����߱�� ID����Ϊ��
);

-- ����ʾ������
INSERT INTO Users (username, password, role, related_id)
VALUES
    ('admin', 'admin123', 'admin', NULL),      -- ����Ա�������
    ('doctor1', 'doctor123', 'doctor', 1),    -- ����ҽ�����е� ID Ϊ 1
    ('patient1', 'patient123', 'patient', 2); -- �������߱��е� ID Ϊ 2
