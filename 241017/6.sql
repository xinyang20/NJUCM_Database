--��������ٿơ�ҽ�����β��˵���ͼ
CREATE VIEW wuguanke_doctor AS
SELECT Cure.pID,pName,sex,Birth
FROM Patient
JOIN Cure ON Cure.pID=Patient.pID
JOIN Doctor ON Doctor.dID=Cure.dID
WHERE Department='��ٿ�'