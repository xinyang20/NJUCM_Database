--统计各科室的就诊费用，要求输出科室名，总费用，输出结果按总费用降序排列
SELECT Doctor.Department,SUM(FEE)
FROM Cure
JOIN Doctor ON Doctor.dID=Cure.dID
GROUP BY Department
ORDER BY SUM(FEE) DESC