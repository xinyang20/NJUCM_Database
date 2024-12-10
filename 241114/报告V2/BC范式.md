为了检查当前数据库的建表设计是否符合 **BCNF（Boyce-Codd Normal Form）** 范式，我们需要回顾各表的结构，并验证它们是否满足 BCNF 的要求。BCNF 是 **第三范式（3NF）** 的一个强化版本，它要求每个非主属性（即不是候选键的一部分）都完全依赖于每个候选键。

### **BCNF 规范总结**

- 一个关系在 BCNF 中，如果它的每个决定因素都是候选键。
- 也就是说，如果表中的属性决定了其他属性的值，决定该属性的那个属性必须是候选键。

### **检查步骤**

我们将逐表检查建表规范，并分析表的主键、外键和依赖关系，确认其是否符合 BCNF 的标准。

------

### **1. 患者表（patients）**

```sql
CREATE TABLE patients (
    patient_id INT PRIMARY KEY IDENTITY(10000001, 1), -- 患者 ID，自动增长，8 位数字
    name VARCHAR(50) NULL,                            -- 患者姓名
    gender VARCHAR(10) NULL CHECK (gender IN ('男', '女')), -- 性别
    age INT NULL,                                     -- 年龄
    contact_number VARCHAR(15) NULL                  -- 联系方式
);
```

- **主键**：`patient_id`
- **非主属性依赖关系**：`name`, `gender`, `age`, `contact_number` 都完全依赖于 `patient_id`。
- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `patient_id`，没有部分依赖或传递依赖。

------

### **2. 医生表（doctors）**

```sql
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,                        -- 医生 ID
    name VARCHAR(50),                                  -- 医生姓名
    gender VARCHAR(10),                                -- 性别
    department VARCHAR(50),                            -- 科室
    title VARCHAR(50),                                 -- 职称
    contact_number VARCHAR(15)                         -- 联系方式
);
```

- **主键**：`doctor_id`
- **非主属性依赖关系**：`name`, `gender`, `department`, `title`, `contact_number` 完全依赖于 `doctor_id`。
- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `doctor_id`。

------

### **3. 处方表（prescriptions）**

```sql
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY,                 -- 处方 ID
    patient_id INT FOREIGN KEY REFERENCES patients(patient_id), -- 关联患者 ID
    doctor_id INT FOREIGN KEY REFERENCES doctors(doctor_id),   -- 关联医生 ID
    date DATETIME DEFAULT GETDATE(),                  -- 开方日期
    amount DECIMAL(10,2),                             -- 处方金额
    usage_instructions TEXT,                          -- 用药指导
    status VARCHAR(20) DEFAULT '待配方',              -- 处方状态
    expected_pickup_time DATETIME NULL                -- 预计取药时间
);
```

- **主键**：`prescription_id`

- 外键依赖

	：

	- `patient_id` 依赖于 `patients` 表。
	- `doctor_id` 依赖于 `doctors` 表。

- **非主属性依赖关系**：`date`, `amount`, `usage_instructions`, `status`, `expected_pickup_time` 完全依赖于 `prescription_id`。

- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `prescription_id`，没有部分依赖或传递依赖。

------

### **4. 任务表（tasks）**

```sql
CREATE TABLE tasks (
    task_id INT PRIMARY KEY IDENTITY(1, 1),           -- 任务 ID，自动增长
    prescription_id INT FOREIGN KEY REFERENCES prescriptions(prescription_id), -- 关联处方 ID
    receive_worker_id INT FOREIGN KEY REFERENCES workers(worker_id), -- 收方工人 ID
    receive_worker_name VARCHAR(50),            -- 收方工人姓名
    form_worker_id INT FOREIGN KEY REFERENCES workers(worker_id), -- 配方工人 ID
    form_worker_name VARCHAR(50),               -- 配方工人姓名
    decoction_worker_id INT FOREIGN KEY REFERENCES workers(worker_id), -- 煎药工人 ID
    decoction_worker_name VARCHAR(50),          -- 煎药工人姓名
    admin_id INT FOREIGN KEY REFERENCES admins(admin_id), -- 任务分配管理员 ID
    admin_name VARCHAR(50),                     -- 任务分配管理员姓名
    receive_time DATETIME NULL,                      -- 处方接收时间
    form_time DATETIME NULL,                         -- 配方时间
    decoction_start_time DATETIME NULL,              -- 煎药开始时间
    decoction_end_time DATETIME NULL,                -- 煎药结束时间
    status VARCHAR(20) DEFAULT '未完成' CHECK (status IN ('未完成', '完成')) -- 任务状态
);
```

- **主键**：`task_id`

- 外键依赖

	：

	- `prescription_id` 依赖于 `prescriptions` 表。
	- `receive_worker_id`, `form_worker_id`, `decoction_worker_id` 依赖于 `workers` 表。
	- `admin_id` 依赖于 `admins` 表。

- **非主属性依赖关系**：所有非主属性（如 `receive_worker_name`, `form_worker_name`, `decoction_worker_name` 等）都依赖于 `task_id`，且不存在部分依赖。

- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `task_id`，没有部分依赖或传递依赖。

------

### **5. 工人表（workers）**

```sql
CREATE TABLE workers (
    worker_id INT PRIMARY KEY,                       -- 工人 ID
    name VARCHAR(50),                                 -- 工人姓名
    age INT,                                          -- 工人年龄
    contact_number VARCHAR(15)                        -- 工人联系方式
);
```

- **主键**：`worker_id`
- **非主属性依赖关系**：`name`, `age`, `contact_number` 完全依赖于 `worker_id`。
- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `worker_id`。

------

### **6. 管理员表（admins）**

```sql
CREATE TABLE admins (
    admin_id INT PRIMARY KEY,                        -- 管理员 ID
    name VARCHAR(50),                                 -- 管理员姓名
    contact_number VARCHAR(15)                        -- 管理员联系方式
);
```

- **主键**：`admin_id`
- **非主属性依赖关系**：`name`, `contact_number` 完全依赖于 `admin_id`。
- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `admin_id`。

------

### **7. 用户表（users）**

```sql
CREATE TABLE users (
    uuid UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(), -- 用户全局唯一标识
    username VARCHAR(50) NOT NULL UNIQUE,             -- 用户名
    password VARCHAR(100) NOT NULL,                   -- 明文密码（开发阶段）
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'doctor', 'patient', 'worker')), -- 用户角色类型
    role_id INT NULL                                  -- 角色表主键 ID，作为外键
);
```

- **主键**：`uuid`
- **非主属性依赖关系**：`username`, `password`, `role`, `role_id` 完全依赖于 `uuid`。
- **结论**：此表符合 **BCNF**，因为所有非主属性完全依赖于主键 `uuid`。

------

### **总结**

根据对现有数据库表的分析，所有表都符合 **BCNF**，因为它们都满足以下条件：

- 所有非主属性都完全依赖于主键，没有部分依赖。
- 每个非主属性都完全依赖于每个候选键。
- 不存在传递依赖。

因此，当前的建表设计符合 **BCNF** 范式。如果您有其他问题，或需要进一步优化某些表的设计，随时告诉我！