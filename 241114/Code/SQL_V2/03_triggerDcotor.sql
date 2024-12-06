-- �����洢���̣����ڲ���ҽ����¼���Զ����� ID
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

    -- ������Ҵ���
    SET @DepartmentCode = CASE @Department
        WHEN '�ڿ�' THEN '01'
        WHEN '���' THEN '02'
        WHEN '����' THEN '03'
        WHEN '����' THEN '04'
        ELSE '00'
    END;

    -- ����ְ�ƴ���
    SET @TitleCode = CASE @Title
        WHEN '����ҽʦ' THEN '01'
        WHEN '������ҽʦ' THEN '02'
        WHEN '����ҽʦ' THEN '03'
        WHEN 'סԺҽʦ' THEN '04'
        ELSE '00'
    END;

    -- ����ҽ�� ID
    SET @GeneratedID = CAST(@DepartmentCode + @TitleCode + FORMAT(NEXT VALUE FOR DoctorIDSequence, '0000') AS INT);

    -- ����ҽ����¼
    INSERT INTO doctors (doctor_id, name, gender, department, title, contact_number)
    VALUES (@GeneratedID, @Name, @Gender, @Department, @Title, @ContactNumber);
END;
GO
-- ɾ��֮ǰ�Ĵ�����������Ѵ��ڣ�
DROP TRIGGER IF EXISTS trg_DoctorID;
GO

-- �����򵥵Ĵ������������Ҫ�����߼���
CREATE TRIGGER trg_DoctorInsert
ON doctors
AFTER INSERT
AS
BEGIN
    PRINT 'ҽ����¼�ѳɹ����롣';
END;
GO
