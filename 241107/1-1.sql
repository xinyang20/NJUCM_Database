--����һ���洢����SInfo��
--��ѯS���й�Ӧ����ν����Ϊ���������й�Ӧ����Ϣ
--����Ӧ�̴��롢��Ӧ����������Ӧ��״̬��
IF EXISTS (
	SELECT NAME FROM SYSOBJECTS
	WHERE NAME='SInfo' AND TYPE='P')
DROP PROCEDURE SInfo
GO
CREATE PROCEDURE SInfo AS
SELECT SNO,SNAME,STATUS
FROM S
WHERE STATUS='20'