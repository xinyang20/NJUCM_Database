--ͳ�Ƹ����ҵľ�����ã�Ҫ��������������ܷ��ã����������ܷ��ý�������
SELECT Doctor.Department,SUM(FEE)
FROM Cure
JOIN Doctor ON Doctor.dID=Cure.dID
GROUP BY Department
ORDER BY SUM(FEE) DESC