-- 触发器：在插入处方后，记录日志
CREATE TRIGGER trg_after_insert_prescriptions
ON Prescriptions
AFTER INSERT
AS
BEGIN
    DECLARE @prescription_id INT;

    -- 遍历 INSERTED 表，逐条获取 prescription_id
    DECLARE inserted_cursor CURSOR FOR
    SELECT prescription_id FROM INSERTED;

    OPEN inserted_cursor;
    FETCH NEXT FROM inserted_cursor INTO @prescription_id;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        PRINT '新处方已创建，处方编号：' + CAST(@prescription_id AS NVARCHAR);
        FETCH NEXT FROM inserted_cursor INTO @prescription_id;
    END;

    CLOSE inserted_cursor;
    DEALLOCATE inserted_cursor;
END;
GO


-- 触发器：更新煎药机器状态
CREATE TRIGGER trg_update_machine_status
ON DecoctionRecords
AFTER INSERT
AS
BEGIN
    UPDATE Machines
    SET machine_status = '使用中'
    WHERE machine_id IN (SELECT machine_id FROM INSERTED);
END;
GO
