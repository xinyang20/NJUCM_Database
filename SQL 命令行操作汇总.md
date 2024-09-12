以下是从四篇实验文档中整理出的所有 SQL 命令行操作及其含义，按照实验步骤记录并使用 Markdown 格式输出。

---

# SQL 命令行操作汇总

## 实验 1：数据库的创建与管理

### 1. 创建数据库
```sql
CREATE DATABASE studb;
```
- **含义**：创建一个名为 `studb` 的数据库。

### 2. 删除数据库
```sql
DROP DATABASE studb;
```
- **含义**：删除名为 `studb` 的数据库。

## 实验 2：数据表的创建与管理

### 1. 创建数据表

#### 创建学生表 `S`
```sql
CREATE TABLE S (
    SNO CHAR(4) PRIMARY KEY,
    SNAME VARCHAR(50),
    AGE INT,
    SEX CHAR(1),
    DNAME VARCHAR(50)
);
```
- **含义**：创建学生表 `S`，包含学号（主键）、姓名、年龄、性别、院系等字段。

#### 创建课程表 `C`
```sql
CREATE TABLE C (
    CNO CHAR(4) PRIMARY KEY,
    CNAME VARCHAR(50),
    CREDIT INT,
    PRE_CNO CHAR(4)
);
```
- **含义**：创建课程表 `C`，包含课程号（主键）、课程名称、学分、先修课程号等字段。

#### 创建成绩表 `SC`
```sql
CREATE TABLE SC (
    SNO CHAR(4),
    CNO CHAR(4),
    SCORE INT,
    PRIMARY KEY (SNO, CNO),
    FOREIGN KEY (SNO) REFERENCES S(SNO),
    FOREIGN KEY (CNO) REFERENCES C(CNO)
);
```
- **含义**：创建成绩表 `SC`，包含学生学号、课程号、成绩。定义了复合主键 `SNO` 和 `CNO`，并设置了外键约束。

### 2. 修改数据表

#### 增加列
```sql
ALTER TABLE S ADD BIRTHDATE DATE;
```
- **含义**：为学生表 `S` 增加一个 `BIRTHDATE` 字段，表示出生日期。

#### 删除列
```sql
ALTER TABLE S DROP COLUMN BIRTHDATE;
```
- **含义**：从学生表 `S` 中删除 `BIRTHDATE` 字段。

### 3. 主键与外键设置

#### 删除主键
```sql
ALTER TABLE SC DROP CONSTRAINT PK_SC;
```
- **含义**：删除成绩表 `SC` 的主键约束。

#### 添加外键
```sql
ALTER TABLE SC ADD CONSTRAINT FK_SC_S FOREIGN KEY (SNO) REFERENCES S(SNO);
```
- **含义**：为成绩表 `SC` 的 `SNO` 字段设置外键，关联学生表 `S` 的 `SNO` 字段。

## 实验 3：数据的插入、修改、删除操作

### 1. 插入数据

#### 向学生表 `S` 插入数据
```sql
INSERT INTO S (SNO, SNAME, AGE, SEX, DNAME) 
VALUES ('S1', '李四', 20, 'M', '计算机');
```
- **含义**：向学生表 `S` 中插入一条记录，表示学生信息。

#### 向课程表 `C` 插入数据
```sql
INSERT INTO C (CNO, CNAME, CREDIT, PRE_CNO) 
VALUES ('C1', '计算机基础', 3, NULL);
```
- **含义**：向课程表 `C` 中插入一条课程记录。

#### 向成绩表 `SC` 插入数据
```sql
INSERT INTO SC (SNO, CNO, SCORE) 
VALUES ('S1', 'C1', 85);
```
- **含义**：向成绩表 `SC` 中插入一条学生成绩记录。

### 2. 修改数据

#### 修改学生表中的年龄
```sql
UPDATE S SET AGE = AGE + 1 WHERE SNO = 'S1';
```
- **含义**：将学生表中学号为 `S1` 的学生年龄加 1。

### 3. 删除数据

#### 删除学生表中的记录
```sql
DELETE FROM S WHERE SNO = 'S10';
```
- **含义**：删除学生表中学号为 `S10` 的学生记录。

### 4. 数据完整性约束检查

#### 插入违反主键约束的数据
```sql
INSERT INTO S (SNO, SNAME, AGE, SEX, DNAME) 
VALUES ('S1', '张三', 21, 'M', '电子');
```
- **含义**：尝试插入一条已存在学号 `S1` 的记录，违反主键约束，操作失败。

#### 插入违反外键约束的数据
```sql
INSERT INTO SC (SNO, CNO, SCORE) 
VALUES ('S10', 'C9', 80);
```
- **含义**：尝试插入一条不存在的课程号 `C9` 的记录，违反外键约束，操作失败。

## 实验 4 和 实验 5：查询和聚合函数操作

### 1. 基本查询

#### 查询学生学号和姓名
```sql
SELECT SNO, SNAME FROM S;
```
- **含义**：查询学生表中的学号和姓名。

### 2. 聚合查询

#### 计算学生的平均成绩
```sql
SELECT AVG(SCORE) FROM SC;
```
- **含义**：计算成绩表中所有学生的平均成绩。

#### 统计选修了某门课程的学生人数
```sql
SELECT COUNT(DISTINCT SNO) FROM SC WHERE CNO = 'C1';
```
- **含义**：统计选修了课程 `C1` 的不同学生人数。

#### 查询每门课程的最高、最低和平均成绩
```sql
SELECT CNO, MAX(SCORE), MIN(SCORE), AVG(SCORE) 
FROM SC 
GROUP BY CNO;
```
- **含义**：查询每门课程的最高成绩、最低成绩和平均成绩，并按课程号分组。

---

通过这些 SQL 命令行操作，实验涵盖了数据库创建、表结构修改、数据插入与删除、查询与聚合等操作，帮助更好地理解 SQL 的核心功能。