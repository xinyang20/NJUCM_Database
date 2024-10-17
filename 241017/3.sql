SELECT Doctor.dID,dName,Patient.pID,pName,FEE
FROM Cure
JOIN Doctor ON Doctor.dID=Cure.dID
JOIN Patient ON Patient.pID=Cure.pID
WHERE Title='主任医生'