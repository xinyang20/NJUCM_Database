-- 禁用外键约束
ALTER TABLE users NOCHECK CONSTRAINT ALL;
ALTER TABLE tasks NOCHECK CONSTRAINT ALL;
ALTER TABLE prescriptions NOCHECK CONSTRAINT ALL;
ALTER TABLE patients NOCHECK CONSTRAINT ALL;
ALTER TABLE doctors NOCHECK CONSTRAINT ALL;
ALTER TABLE workers NOCHECK CONSTRAINT ALL;
ALTER TABLE admins NOCHECK CONSTRAINT ALL;
GO

-- 清空表数据
DELETE FROM users;
DELETE FROM tasks;
DELETE FROM prescriptions;
DELETE FROM doctors;
DELETE FROM patients;
DELETE FROM workers;
DELETE FROM admins;

-- 重置自增 ID，从 1 开始
DBCC CHECKIDENT ('patients', RESEED, 0);
DBCC CHECKIDENT ('workers', RESEED, 0);
DBCC CHECKIDENT ('admins', RESEED, 0);
DBCC CHECKIDENT ('prescriptions', RESEED, 0);
DBCC CHECKIDENT ('tasks', RESEED, 0);
GO

INSERT INTO patients (name, gender, age, contact_number)
VALUES 
('张三', '男', 30, '12345678906'),
('李四', '女', 28, '12345678907'),
('王五', '男', 35, '12345678908'),
('赵六', '女', 22, '12345678909'),
('钱七', '男', 40, '12345678910'),
('孙八', '女', 32, '12345678911'),
('周九', '男', 25, '12345678912'),
('吴十', '女', 27, '12345678913'),
('郑十一', '男', 38, '12345678914'),
('王十二', '女', 29, '12345678915');
GO

INSERT INTO doctors (doctor_id, name, gender, department, title, contact_number)
VALUES 
(10101001, '李四', '男', '内科', '主任医师', '12345678901'),
(10101002, '王五', '女', '内科', '副主任医师', '12345678902'),
(10202001, '赵六', '男', '外科', '主任医师', '12345678903'),
(10202002, '钱七', '男', '外科', '主治医师', '12345678904'),
(10202003, '孙八', '女', '外科', '住院医师', '12345678905');
GO

INSERT INTO workers (name, age, contact_number)
VALUES 
('工人1', 28, '12345678916'),
('工人2', 35, '12345678917'),
('工人3', 26, '12345678918'),
('工人4', 40, '12345678919'),
('工人5', 30, '12345678920');
GO

INSERT INTO admins (name, contact_number)
VALUES 
('管理员1', '12345678921'),
('管理员2', '12345678922'),
('管理员3', '12345678923');
GO

INSERT INTO prescriptions (patient_id, doctor_id, date, amount, usage_instructions, status)
VALUES
(1, 10101001, GETDATE(), 100.50, '每日两次', '待配方'),
(2, 10101002, GETDATE(), 200.75, '每日三次', '待配方'),
(3, 10202001, GETDATE(), 150.00, '每日一次', '待配方'),
(4, 10202002, GETDATE(), 250.25, '每日四次', '待配方'),
(5, 10202003, GETDATE(), 300.00, '每日两次', '待配方'),
(6, 10101001, GETDATE(), 120.50, '每晚服用', '待配方'),
(7, 10101002, GETDATE(), 220.75, '饭后服用', '待配方'),
(8, 10202001, GETDATE(), 180.00, '每日两次', '待配方'),
(9, 10202002, GETDATE(), 260.25, '晨起服用', '待配方'),
(10, 10202003, GETDATE(), 310.00, '每日一次', '待配方');
GO

-- 仅插入 prescription_id，其他字段置空
INSERT INTO tasks (prescription_id, status)
VALUES
(1, '未完成'),
(2, '未完成'),
(3, '未完成'),
(4, '未完成'),
(5, '未完成');
GO

-- 插入用户记录
INSERT INTO users (username, password, role, role_id)
VALUES 
-- 关联医生
('doctor1', '123456', 'doctor', 10101001),
('doctor2', '123456', 'doctor', 10101002),
('doctor3', '123456', 'doctor', 10202001),
('doctor4', '123456', 'doctor', 10202002),
('doctor5', '123456', 'doctor', 10202003),
-- 关联患者
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
-- 关联管理员
('admin1', '123456', 'admin', 1),
('admin2', '123456', 'admin', 2),
('admin3', '123456', 'admin', 3),
-- 关联工人
('worker1', '123456', 'worker', 1),
('worker2', '123456', 'worker', 2),
('worker3', '123456', 'worker', 3),
('worker4', '123456', 'worker', 4),
('worker5', '123456', 'worker', 5);
GO

-- 启用外键约束
ALTER TABLE users CHECK CONSTRAINT ALL;
ALTER TABLE tasks CHECK CONSTRAINT ALL;
ALTER TABLE prescriptions CHECK CONSTRAINT ALL;
ALTER TABLE patients CHECK CONSTRAINT ALL;
ALTER TABLE doctors CHECK CONSTRAINT ALL;
ALTER TABLE workers CHECK CONSTRAINT ALL;
ALTER TABLE admins CHECK CONSTRAINT ALL;
GO
