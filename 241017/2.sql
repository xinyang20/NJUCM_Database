--查询与医生王丹在同一个科室的医生编号和姓名
SELECT dID,dNAME
FROM Doctor
WHERE Department=(
	SELECT Department
	FROM Doctor
	WHERE dName='王丹')