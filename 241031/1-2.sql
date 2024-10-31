DECLARE @sname char(8), @cname varchar(24)
EXEC get_sc_name 'S1','C3',@sname OUTPUT,@cname OUTPUT;
SELECT SNAME=@sname,CNAME=@cname;

EXEC get_sc_name 'S1','C3',@sname OUTPUT,@cname OUTPUT;
SELECT SNAME=@sname,CNAME=@cname;

EXEC get_sc_name 'S30','C4',@sname OUTPUT,@cname OUTPUT;
SELECT SNAME=@sname,CNAME=@cname;