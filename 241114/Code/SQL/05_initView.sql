-- 创建患者视图
CREATE VIEW PatientView AS
SELECT Prescriptions.prescription_id, prescription_date, pickup_method, expected_pickup_time, actual_pickup_time
FROM Prescriptions,DecoctionRecords
WHERE patient_id = SESSION_USER AND Prescriptions.prescription_id=DecoctionRecords.prescription_id;
GO

-- 创建医生视图
CREATE VIEW DoctorView AS
SELECT prescription_id, patient_id, prescription_date, usage_instructions
FROM Prescriptions
WHERE doctor_id = SESSION_USER;
GO

-- 创建药房管理员视图
CREATE VIEW PharmacyAdminView AS
SELECT machine_id, machine_status
FROM Machines;
GO

-- 创建操作员视图
CREATE VIEW OperatorView AS
SELECT decoction_id, prescription_id, formulation_staff, decoction_staff, print_staff
FROM DecoctionRecords;
