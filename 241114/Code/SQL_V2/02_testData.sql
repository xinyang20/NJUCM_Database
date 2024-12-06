-- �������Լ��
ALTER TABLE users NOCHECK CONSTRAINT ALL;
ALTER TABLE tasks NOCHECK CONSTRAINT ALL;
ALTER TABLE prescriptions NOCHECK CONSTRAINT ALL;
ALTER TABLE patients NOCHECK CONSTRAINT ALL;
ALTER TABLE doctors NOCHECK CONSTRAINT ALL;
ALTER TABLE workers NOCHECK CONSTRAINT ALL;
ALTER TABLE admins NOCHECK CONSTRAINT ALL;
GO

-- ��ձ�����
DELETE FROM users;
DELETE FROM tasks;
DELETE FROM prescriptions;
DELETE FROM doctors;
DELETE FROM patients;
DELETE FROM workers;
DELETE FROM admins;

-- �������� ID���� 1 ��ʼ
DBCC CHECKIDENT ('patients', RESEED, 0);
DBCC CHECKIDENT ('workers', RESEED, 0);
DBCC CHECKIDENT ('admins', RESEED, 0);
DBCC CHECKIDENT ('prescriptions', RESEED, 0);
DBCC CHECKIDENT ('tasks', RESEED, 0);
GO

INSERT INTO patients (name, gender, age, contact_number)
VALUES 
('����', '��', 30, '12345678906'),
('����', 'Ů', 28, '12345678907'),
('����', '��', 35, '12345678908'),
('����', 'Ů', 22, '12345678909'),
('Ǯ��', '��', 40, '12345678910'),
('���', 'Ů', 32, '12345678911'),
('�ܾ�', '��', 25, '12345678912'),
('��ʮ', 'Ů', 27, '12345678913'),
('֣ʮһ', '��', 38, '12345678914'),
('��ʮ��', 'Ů', 29, '12345678915');
GO

INSERT INTO doctors (doctor_id, name, gender, department, title, contact_number)
VALUES 
(10101001, '����', '��', '�ڿ�', '����ҽʦ', '12345678901'),
(10101002, '����', 'Ů', '�ڿ�', '������ҽʦ', '12345678902'),
(10202001, '����', '��', '���', '����ҽʦ', '12345678903'),
(10202002, 'Ǯ��', '��', '���', '����ҽʦ', '12345678904'),
(10202003, '���', 'Ů', '���', 'סԺҽʦ', '12345678905');
GO

INSERT INTO workers (name, age, contact_number)
VALUES 
('����1', 28, '12345678916'),
('����2', 35, '12345678917'),
('����3', 26, '12345678918'),
('����4', 40, '12345678919'),
('����5', 30, '12345678920');
GO

INSERT INTO admins (name, contact_number)
VALUES 
('����Ա1', '12345678921'),
('����Ա2', '12345678922'),
('����Ա3', '12345678923');
GO

INSERT INTO prescriptions (patient_id, doctor_id, date, amount, usage_instructions, status)
VALUES
(1, 10101001, GETDATE(), 100.50, 'ÿ������', '���䷽'),
(2, 10101002, GETDATE(), 200.75, 'ÿ������', '���䷽'),
(3, 10202001, GETDATE(), 150.00, 'ÿ��һ��', '���䷽'),
(4, 10202002, GETDATE(), 250.25, 'ÿ���Ĵ�', '���䷽'),
(5, 10202003, GETDATE(), 300.00, 'ÿ������', '���䷽'),
(6, 10101001, GETDATE(), 120.50, 'ÿ�����', '���䷽'),
(7, 10101002, GETDATE(), 220.75, '�������', '���䷽'),
(8, 10202001, GETDATE(), 180.00, 'ÿ������', '���䷽'),
(9, 10202002, GETDATE(), 260.25, '�������', '���䷽'),
(10, 10202003, GETDATE(), 310.00, 'ÿ��һ��', '���䷽');
GO

-- ������ prescription_id�������ֶ��ÿ�
INSERT INTO tasks (prescription_id, status)
VALUES
(1, 'δ���'),
(2, 'δ���'),
(3, 'δ���'),
(4, 'δ���'),
(5, 'δ���');
GO

-- �����û���¼
INSERT INTO users (username, password, role, role_id)
VALUES 
-- ����ҽ��
('doctor1', '123456', 'doctor', 10101001),
('doctor2', '123456', 'doctor', 10101002),
('doctor3', '123456', 'doctor', 10202001),
('doctor4', '123456', 'doctor', 10202002),
('doctor5', '123456', 'doctor', 10202003),
-- ��������
('patient1', '123456', 'patient', 1),
('patient2', '123456', 'patient', 2),
('patient3', '123456', 'patient', 3),
('patient4', '123456', 'patient', 4),
('patient5', '123456', 'patient', 5),
('patient6', '123456', 'patient', 6),
('patient7', '123456', 'patient', 7),
('patient8', '123456', 'patient', 8),
('patient9', '123456', 'patient', 9),
('patient10', '123456', 'patient', 10),
-- ��������Ա
('admin1', '123456', 'admin', 1),
('admin2', '123456', 'admin', 2),
('admin3', '123456', 'admin', 3),
-- ��������
('worker1', '123456', 'worker', 1),
('worker2', '123456', 'worker', 2),
('worker3', '123456', 'worker', 3),
('worker4', '123456', 'worker', 4),
('worker5', '123456', 'worker', 5);
GO

-- �������Լ��
ALTER TABLE users CHECK CONSTRAINT ALL;
ALTER TABLE tasks CHECK CONSTRAINT ALL;
ALTER TABLE prescriptions CHECK CONSTRAINT ALL;
ALTER TABLE patients CHECK CONSTRAINT ALL;
ALTER TABLE doctors CHECK CONSTRAINT ALL;
ALTER TABLE workers CHECK CONSTRAINT ALL;
ALTER TABLE admins CHECK CONSTRAINT ALL;
GO
