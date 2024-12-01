-- 存储过程：查询某患者的历史处方
CREATE PROCEDURE sp_get_patient_history
    @patient_id INT
AS
BEGIN
    SELECT * FROM Prescriptions WHERE patient_id = @patient_id;
END;
GO

-- 存储过程：更新煎药机器状态
CREATE PROCEDURE sp_update_machine_status
    @machine_id INT,
    @new_status VARCHAR(20)
AS
BEGIN
    UPDATE Machines
    SET machine_status = @new_status
    WHERE machine_id = @machine_id;
END;
