-- 创建存储过程，用于插入医生记录并自动生成 ID
CREATE PROCEDURE InsertDoctor
    @Name NVARCHAR(50),
    @Gender NVARCHAR(10),
    @Department NVARCHAR(50),
    @Title NVARCHAR(50),
    @ContactNumber NVARCHAR(15)
AS
BEGIN
    DECLARE @DepartmentCode NVARCHAR(2);
    DECLARE @TitleCode NVARCHAR(2);
    DECLARE @GeneratedID INT;

    -- 计算科室代码
    SET @DepartmentCode = CASE @Department
        WHEN '内科' THEN '01'
        WHEN '外科' THEN '02'
        WHEN '儿科' THEN '03'
        WHEN '妇科' THEN '04'
        ELSE '00'
    END;

    -- 计算职称代码
    SET @TitleCode = CASE @Title
        WHEN '主任医师' THEN '01'
        WHEN '副主任医师' THEN '02'
        WHEN '主治医师' THEN '03'
        WHEN '住院医师' THEN '04'
        ELSE '00'
    END;

    -- 生成医生 ID
    SET @GeneratedID = CAST(@DepartmentCode + @TitleCode + FORMAT(NEXT VALUE FOR DoctorIDSequence, '0000') AS INT);

    -- 插入医生记录
    INSERT INTO doctors (doctor_id, name, gender, department, title, contact_number)
    VALUES (@GeneratedID, @Name, @Gender, @Department, @Title, @ContactNumber);
END;
GO
-- 删除之前的触发器（如果已存在）
DROP TRIGGER IF EXISTS trg_DoctorID;
GO

-- 创建简单的触发器（如果需要其他逻辑）
CREATE TRIGGER trg_DoctorInsert
ON doctors
AFTER INSERT
AS
BEGIN
    PRINT '医生记录已成功插入。';
END;
GO
