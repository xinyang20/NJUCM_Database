insert into C(CNO,CNAME,CREDIT,PRE_CNO)values('C1','计算机基础',3,'');
insert into C(CNO,CNAME,CREDIT,PRE_CNO)values('C2','C语言',3,'C1');
insert into C(CNO,CNAME,CREDIT,PRE_CNO)values('C3','电子学',4,'C1');
insert into C(CNO,CNAME,CREDIT,PRE_CNO)values('C4','数据结构',4,'C2');

insert into SC(SNO,CNO,SCORE)values('S3','C3',87);
insert into SC(SNO,CNO,SCORE)values('S4','C3',79);
insert into SC(SNO,CNO,SCORE)values('S1','C2',88);
insert into SC(SNO,CNO,SCORE)values('S9','C4',83);
insert into SC(SNO,CNO,SCORE)values('S1','C3',76);
insert into SC(SNO,CNO,SCORE)values('S6','C3',68);
insert into SC(SNO,CNO,SCORE)values('S1','C1',78);
insert into SC(SNO,CNO,SCORE)values('S6','C1',88);
insert into SC(SNO,CNO,SCORE)values('S3','C2',64);
insert into SC(SNO,CNO,SCORE)values('S1','C4',86);
insert into SC(SNO,CNO,SCORE)values('S9','C2',78);