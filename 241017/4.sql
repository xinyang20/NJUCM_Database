--ͳ��ÿ��ҽ�����β��˵�ƽ���������
SELECT dName,AVG(FEE)
FROM Cure
JOIN Doctor ON Doctor.dID=Cure.dID
GROUP BY Cure.dID,Doctor.dName