CREATE PROCEDURE get_sc_name
@sno char(6), 
@cno char(2), 
@sname char(8) OUTPUT, 
@cname varchar(24) OUTPUT 
AS
SELECT @sname=SNAME, @cname=CNAME
FROM S,C,SC
WHERE S.SNO=SC.SNO AND C.CNO=SC.CNO AND SC.SNO=@sno AND SC.CNO=@cno