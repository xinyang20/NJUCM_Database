--查询就诊费用超过500元的病人的基本信息及就诊总费用
SELECT Patient.*,Fee
FROM Patient
JOIN Cure ON Patient.pID=Cure.pID
GROUP BY Patient.pID,Cure.Fee,Patient.pName,Patient.sex,Patient.Birth
HAVING FEE>500