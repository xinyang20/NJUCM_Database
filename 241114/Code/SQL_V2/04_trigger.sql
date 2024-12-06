-- ɾ��������
DROP TRIGGER IF EXISTS trg_CreateTaskOnPrescriptionInsert;
GO

-- �������������������´���ʱ�Զ����ɶ�Ӧ����
CREATE TRIGGER trg_CreateTaskOnPrescriptionInsert
ON prescriptions
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- ���������񣬹������²���Ĵ���
    INSERT INTO tasks (prescription_id, status)
    SELECT 
        i.prescription_id,
        'δ���'
    FROM 
        inserted i;

    SET NOCOUNT OFF;
END;
GO
