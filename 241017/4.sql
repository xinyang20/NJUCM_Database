--统计每个医生诊治病人的平均就诊费用
SELECT dName,AVG(FEE)
FROM Cure
JOIN Doctor ON Doctor.dID=Cure.dID
GROUP BY Cure.dID,Doctor.dName