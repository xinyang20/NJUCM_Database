-- 创建操作日志表
CREATE TABLE OperationLogs (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    operation_time DATETIME NOT NULL DEFAULT GETDATE(),
    user_name NVARCHAR(50) NOT NULL,
    operation NVARCHAR(200) NOT NULL
);
GO

-- 在触发器中记录操作
CREATE TRIGGER trg_log_operations
ON DecoctionRecords
AFTER INSERT
AS
BEGIN
    INSERT INTO OperationLogs (user_name, operation)
    VALUES (SESSION_USER, '插入新的煎药记录');
END;
