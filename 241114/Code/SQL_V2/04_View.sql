--患者视图
CREATE VIEW PatientView AS
SELECT prescription_id, date, status, usage_instructions, expected_pickup_time
FROM prescriptions
WHERE patient_id = CURRENT_USER;
GO

--医生视图
CREATE VIEW DoctorView AS
SELECT prescription_id, patient_id, date, status, usage_instructions
FROM prescriptions
WHERE doctor_id = CURRENT_USER;
GO

--工人视图
CREATE VIEW WorkerView AS
SELECT task_id, prescription_id, receive_worker_name, form_worker_name, decoction_worker_name, receive_time, form_time, decoction_start_time, decoction_end_time, status
FROM tasks;
GO