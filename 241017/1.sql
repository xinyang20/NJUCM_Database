--��ѯ������ó���500Ԫ�Ĳ��˵Ļ�����Ϣ�������ܷ���
SELECT Patient.*,Fee
FROM Patient
JOIN Cure ON Patient.pID=Cure.pID
GROUP BY Patient.pID,Cure.Fee,Patient.pName,Patient.sex,Patient.Birth
HAVING FEE>500