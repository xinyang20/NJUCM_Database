--���� INSTEAD OF ��������
--��J���ϴ���һ��ɾ�����͵Ĵ����� TR_NotAllowDelete��
--����J����ɾ����¼ʱ�������ô�������
--��ʾ������ɾ���������ݵ���ʾ��Ϣ
IF EXISTS (SELECT NAME FROM SYSOBJECTS 
			WHERE NAME='TR_NotAllowDelete' AND TYPE='TR')
DROP TRIGGER TR_NotAllowDelete
GO

CREATE TRIGGER TR_NotAllowDelete ON J AFTER DELETE
AS PRINT '�����е����ݲ�����ɾ��'
ROLLBACK
GO