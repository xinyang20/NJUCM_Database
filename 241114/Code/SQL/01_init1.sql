-- �������ݿ�
CREATE DATABASE DecoctionSystem;
GO

-- ʹ�����ݿ�
USE DecoctionSystem;
GO

-- ����������Ϣ��
CREATE TABLE Patients (
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(15) NOT NULL CHECK (LEN(contact_number) >= 10)
);
GO

-- ����ҽ����Ϣ��
CREATE TABLE Doctors (
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    doctor_name VARCHAR(50) NOT NULL,
    department_name VARCHAR(50) NOT NULL
);
GO

-- ����������
CREATE TABLE Prescriptions (
    prescription_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL FOREIGN KEY REFERENCES Patients(patient_id),
    doctor_id INT NOT NULL FOREIGN KEY REFERENCES Doctors(doctor_id),
    pickup_method VARCHAR(20) CHECK (pickup_method IN ('��ȡ', '����')) NOT NULL,
    prescription_date DATE NOT NULL,
    prescription_amount DECIMAL(10,2) CHECK (prescription_amount >= 0) NOT NULL,
    prescription_weight FLOAT CHECK (prescription_weight >= 0) NOT NULL,
    dose_count INT CHECK (dose_count >= 0) NOT NULL,
    usage_instructions TEXT NOT NULL,
    expected_pickup_time DATETIME NOT NULL
);
GO

-- ������ҩ������
CREATE TABLE Machines (
    machine_id INT IDENTITY(1,1) PRIMARY KEY,
    machine_status VARCHAR(20) CHECK (machine_status IN ('����', 'ʹ����', 'ά����')) NOT NULL
);
GO

-- ������ҩ��¼��
CREATE TABLE DecoctionRecords (
    decoction_id INT IDENTITY(1,1) PRIMARY KEY,
    prescription_id INT NOT NULL FOREIGN KEY REFERENCES Prescriptions(prescription_id),
    pickup_date DATE NOT NULL,
    formulation_staff VARCHAR(50) NOT NULL,
    formulation_date DATETIME NOT NULL,
    soaking_staff VARCHAR(50),
    soaking_start_time DATETIME,
    soaking_end_time DATETIME,
    decoction_staff VARCHAR(50) NOT NULL,
    decoction_start_time DATETIME NOT NULL,
    decoction_end_time DATETIME NOT NULL,
    print_staff VARCHAR(50) NOT NULL,
    print_time DATETIME NOT NULL,
    actual_pickup_time DATETIME
);
GO

-- �����Ż�
-- Ϊ������ѯ�����ӵ��ֶ��������
CREATE INDEX idx_patient_contact ON Patients(contact_number);
CREATE INDEX idx_prescription_date ON Prescriptions(prescription_date);
CREATE INDEX idx_expected_pickup_time ON Prescriptions(expected_pickup_time);
CREATE INDEX idx_machine_status ON Machines(machine_status);

-- Ϊ�ۼ�����ʹ�õ��ֶ��������
CREATE INDEX idx_prescription_amount ON Prescriptions(prescription_amount);
CREATE INDEX idx_prescription_weight ON Prescriptions(prescription_weight);
CREATE INDEX idx_dose_count ON Prescriptions(dose_count);

-- ��ɽ������������
PRINT '���ݿ�ͱ�ṹ�ѳɹ�����';
GO
