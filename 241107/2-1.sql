--����AFTER��������
--��SPJ���ϴ���һ�����롢�������͵Ĵ�����TR_QTYCheck,
--���� QTY �ֶ��в�����޸Ŀ��Է�����,
--�����ô��������������Ƿ��� 0-10000 ֮�䡣
IF EXISTS(SELECT NAME FROM SYSOBJECTS 
WHERE NAME='TR_QTYCheck' AND TYPE='TR')
DROP TRIGGER TR_QTYCheck
GO
CREATE TRIGGER TR_QTYCheck ON SPJ
FOR INSERT,UPDATE AS
IF UPDATE(QTY) PRINT 'AFTER��������ʼִ�С���'
BEGIN
	DECLARE @QTY REAL
	SELECT @QTY=(SELECT QTY FROM INSERTED)
	IF @QTY<0 OR @QTY>1000
	PRINT '���������������ȷ����������������'
END
GO