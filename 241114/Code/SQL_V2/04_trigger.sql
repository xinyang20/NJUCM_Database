-- 删除触发器
DROP TRIGGER IF EXISTS trg_CreateTaskOnPrescriptionInsert;
GO

-- 创建触发器，当插入新处方时自动生成对应任务
CREATE TRIGGER trg_CreateTaskOnPrescriptionInsert
ON prescriptions
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- 插入新任务，关联到新插入的处方
    INSERT INTO tasks (prescription_id, status)
    SELECT 
        i.prescription_id,
        '未完成'
    FROM 
        inserted i;

    SET NOCOUNT OFF;
END;
GO
