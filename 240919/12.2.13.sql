SELECT SC.SNO AS 'ѧ��',AVG(SCORE) AS 'ƽ���ɼ�'
FROM SC,S
WHERE S.SNO=SC.SNO AND DNAME='�����'--����û����ѧϵ������ʹ�ü����ϵ����
GROUP BY SC.SNO
HAVING AVG(SCORE)>80 