CREATE TABLE Appointments (
    appointment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL FOREIGN KEY REFERENCES Patients(patient_id),
    doctor_id INT NOT NULL FOREIGN KEY REFERENCES Doctors(doctor_id),
    appointment_date DATETIME DEFAULT GETDATE()
);
