--建立“五官科”医生诊治病人的视图
CREATE VIEW wuguanke_doctor AS
SELECT Cure.pID,pName,sex,Birth
FROM Patient
JOIN Cure ON Cure.pID=Patient.pID
JOIN Doctor ON Doctor.dID=Cure.dID
WHERE Department='五官科'