DECLARE @dt1 DATETIME
DECLARE @i INT
DECLARE @s CHAR(40)
DECLARE @hm1 INT
DECLARE @hm2 INT
SELECT @dt1=GETDATE()
SELECT @hm1=DATEPART(hh,@dt1)*3600000+DATEPART(mi,@dt1)*60000+DATEPART(ss,@dt1)*1000+DATEPART(ms,@dt1)

--���н��ò����������
--CREATE NONCLUSTERED INDEX indexname1 ON itb1(id)--����id�Ǿۼ�����
--CREATE NONCLUSTERED INDEX indexname1 ON itb1(mm)--����mm�Ǿۼ�����
--CREATE CLUSTERED INDEX indexname1 ON itb1(id)--����id�ۼ�����
--CREATE CLUSTERED INDEX indexname1 ON itb1(mm)--����mm�ۼ�����
DROP INDEX itb1.indexname1--ɾ������


SELECT @dt1=GETDATE()
SELECT @hm2=DATEPART(hh,@dt1)*3600000+DATEPART(mi,@dt1)*60000+DATEPART(ss,@dt1)*1000+DATEPART(ms,@dt1)-@hm1
SELECT @s='time--'+CONVERT(char(10),@hm2)
RAISERROR(@s,16,1)