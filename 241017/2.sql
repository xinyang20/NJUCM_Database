--��ѯ��ҽ��������ͬһ�����ҵ�ҽ����ź�����
SELECT dID,dNAME
FROM Doctor
WHERE Department=(
	SELECT Department
	FROM Doctor
	WHERE dName='����')