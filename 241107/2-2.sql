--创建 INSTEAD OF 触发器：
--在J表上创建一个删除类型的触发器 TR_NotAllowDelete，
--当在J表中删除记录时，触发该触发器，
--显示不允许删除表中数据的提示信息
IF EXISTS (SELECT NAME FROM SYSOBJECTS 
			WHERE NAME='TR_NotAllowDelete' AND TYPE='TR')
DROP TRIGGER TR_NotAllowDelete
GO

CREATE TRIGGER TR_NotAllowDelete ON J AFTER DELETE
AS PRINT '本表中的数据不允许被删除'
ROLLBACK
GO