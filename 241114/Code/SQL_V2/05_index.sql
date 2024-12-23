-- ��������
-- ������Ϊ�����ֶε�����
CREATE INDEX idx_patient_id ON prescriptions(patient_id);
CREATE INDEX idx_doctor_id ON prescriptions(doctor_id);
CREATE INDEX idx_prescription_id ON tasks(prescription_id);

-- ������Ϊ��ѯ����������
CREATE INDEX idx_contact_number_patients ON patients(contact_number);
CREATE INDEX idx_contact_number_workers ON workers(contact_number);
CREATE INDEX idx_prescription_date ON prescriptions(date);
CREATE INDEX idx_prescription_status ON prescriptions(status);
CREATE INDEX idx_task_status ON tasks(status);
CREATE INDEX idx_expected_pickup_time ON prescriptions(expected_pickup_time);

-- ������Ϊ�ۼ���������������
CREATE INDEX idx_amount ON prescriptions(amount);