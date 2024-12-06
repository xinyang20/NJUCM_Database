from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# 初始化 Flask 应用
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 替换为更安全的密钥
password='20050317'

# 配置 SQL Server 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://sa:{password}@localhost/DecoctionSystem?driver=ODBC+Driver+17+for+SQL+Server'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    __tablename__ = 'Users'
    account_id = db.Column(db.Integer, primary_key=True)  # 自动递增的账号 ID
    username = db.Column(db.String(50), nullable=False, unique=True)  # 用户名
    password = db.Column(db.String(100), nullable=False)  # 密码
    role = db.Column(db.String(50), nullable=False)  # 用户角色（admin、doctor、patient）
    related_id = db.Column(db.Integer, nullable=True)  # 关联医生或患者表的 ID

class Doctor(db.Model):
    __tablename__ = 'Doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(50), nullable=False)
    department_name = db.Column(db.String(50), nullable=False)

class Patient(db.Model):
    __tablename__ = 'Patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)

class Appointment(db.Model):
    __tablename__ = 'Appointments'

    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.doctor_id'), nullable=False)
    appointment_date = db.Column(db.DateTime, default=datetime.utcnow)


class Prescription(db.Model):
    __tablename__ = 'Prescriptions'

    prescription_id = db.Column(db.Integer, primary_key=True)  # 处方ID
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.patient_id'), nullable=False)  # 患者ID
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.doctor_id'), nullable=False)  # 医生ID
    pickup_method = db.Column(db.String(20), nullable=False)  # 取药方式
    prescription_date = db.Column(db.Date, nullable=False)  # 处方日期
    prescription_amount = db.Column(db.Numeric(10, 2), nullable=False)  # 处方金额
    prescription_weight = db.Column(db.Float, nullable=False)  # 药材总重量
    dose_count = db.Column(db.Integer, nullable=False)  # 剂数
    usage_instructions = db.Column(db.Text, nullable=False)  # 用法说明
    expected_pickup_time = db.Column(db.DateTime, nullable=False)  # 预期取药时间

    # 可选：建立与 `Patient` 和 `Doctor` 模型的关系
    patient = db.relationship('Patient', backref='prescriptions', lazy=True)
    doctor = db.relationship('Doctor', backref='prescriptions', lazy=True)

class DecoctionRecord(db.Model):
    __tablename__ = 'DecoctionRecords'

    decoction_id = db.Column(db.Integer, primary_key=True)  # 煎药记录ID
    prescription_id = db.Column(db.Integer, db.ForeignKey('Prescriptions.prescription_id'), nullable=False)  # 关联处方ID
    pickup_date = db.Column(db.Date, nullable=False)  # 取药日期
    formulation_staff = db.Column(db.String(50), nullable=False)  # 配方人员
    formulation_date = db.Column(db.DateTime, nullable=False)  # 配方日期时间
    soaking_staff = db.Column(db.String(50))  # 浸泡人员
    soaking_start_time = db.Column(db.DateTime)  # 浸泡开始时间
    soaking_end_time = db.Column(db.DateTime)  # 浸泡结束时间
    decoction_staff = db.Column(db.String(50), nullable=False)  # 煎药人员
    decoction_start_time = db.Column(db.DateTime, nullable=False)  # 煎药开始时间
    decoction_end_time = db.Column(db.DateTime, nullable=False)  # 煎药结束时间
    print_staff = db.Column(db.String(50), nullable=False)  # 打印标签人员
    print_time = db.Column(db.DateTime, nullable=False)  # 打印时间
    actual_pickup_time = db.Column(db.DateTime)  # 实际取药时间

    # 与 Prescription 的关系
    prescription = db.relationship('Prescription', backref='decoction_record', lazy=True)

# 首页
@app.route('/')
def home():
    if 'user_id' in session:
        role = session.get('role')
        username = session.get('username')
        welcome_message = f"您好，{username}，欢迎来到中药管理系统！"

        # 根据角色定义权限
        if role == 'decoction_worker':
            is_factory_manager = session.get('is_factory_manager', False)
            if is_factory_manager:
                welcome_message += "<br>您拥有工厂管理权限。"
            else:
                welcome_message += "<br>祝您工作愉快！"

        elif role == 'admin':
            welcome_message = f"您好，管理员 {username}！"

        elif role == 'doctor':
            doctor = Doctor.query.filter_by(doctor_id=session.get('related_id')).first()
            if doctor:
                welcome_message = f"你好，{doctor.doctor_name}（{doctor.department_name}）<br>祝您工作愉快！"

        elif role == 'patient':
            patient = Patient.query.filter_by(patient_id=session.get('related_id')).first()
            if patient:
                welcome_message = f"您好，{patient.patient_name}<br>祝您早日康复！"

        return render_template(
            'dashboard.html',
            username=username,
            role=role,
            welcome_message=welcome_message,
            is_factory_manager=session.get('is_factory_manager', False)
        )
    return redirect(url_for('login'))



# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 验证用户
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.account_id
            session['username'] = user.username
            session['role'] = user.role
            session['related_id'] = user.related_id  # 存储关联的医生或患者 ID

            # 如果是工人，检查是否具有工厂管理权限
            session['is_factory_manager'] = (user.role == 'decoction_worker' and user.related_id == 0)

            flash('登录成功!', 'success')
            return redirect(url_for('home'))
        else:
            flash('用户名或密码错误!', 'danger')

    return render_template('login.html')

# 注销功能
@app.route('/logout')
def logout():
    session.clear()
    flash('已注销!', 'info')
    return redirect(url_for('login'))

# 管理员查看所有信息
@app.route('/admin/all')
def admin_all():
    if 'user_id' in session and session.get('role') == 'admin':
        users = User.query.all()
        patients = db.session.execute(text('SELECT * FROM Patients')).fetchall()
        doctors = db.session.execute(text('SELECT * FROM Doctors')).fetchall()
        return render_template(
            'admin_all.html',
            users=users,
            patients=patients,
            doctors=doctors
        )
    else:
        flash('您没有权限查看此页面!', 'warning')
        return redirect(url_for('home'))

# 医生查看个人信息
@app.route('/doctor/info')
def doctor_info():
    if 'user_id' in session and session.get('role') == 'doctor':
        doctor_id = session['related_id']  # 从 session 获取医生 ID
        doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()  # 查询医生信息
        if not doctor:
            flash('未找到医生信息!', 'warning')
            return redirect(url_for('home'))
        return render_template('doctor_info.html', doctor=doctor)
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 医生查看患者信息
@app.route('/doctor/patients')
def doctor_patients():
    if 'user_id' in session and session.get('role') == 'doctor':
        doctor_id = session['related_id']  # 从 session 中获取关联的医生 ID
        patients = db.session.execute(
            text('''
            SELECT DISTINCT p.*
            FROM Patients p
            JOIN Prescriptions ps ON p.patient_id = ps.patient_id
            WHERE ps.doctor_id = :doctor_id
            '''),
            {'doctor_id': doctor_id}
        ).fetchall()
        return render_template('doctor_patients.html', patients=patients)
    else:
        flash('您没有权限查看此页面!', 'warning')
        return redirect(url_for('home'))

# 患者查看个人信息
@app.route('/patient/personal_info')
def patient_personal_info():
    if 'user_id' in session and session.get('role') == 'patient':
        patient_id = session['related_id']
        personal_info = Patient.query.filter_by(patient_id=patient_id).first()
        account_id = session['user_id']
        return render_template(
            'patient_personal_info.html',
            personal_info=personal_info,
            account_id=account_id
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 患者修改进行挂号
@app.route('/patient/appointment', methods=['GET', 'POST'])
def patient_appointment():
    if 'user_id' in session and session.get('role') == 'patient':
        query = Doctor.query  # 初始化查询对象
        # 查询所有科室名称
        departments = db.session.query(Doctor.department_name).distinct().order_by(Doctor.department_name).all()
        department_list = [d.department_name for d in departments]

        if request.method == 'POST':
            search_query = request.form.get('search_query')
            selected_department = request.form.get('selected_department')

            # 按医生名称过滤
            if search_query:
                query = query.filter(Doctor.doctor_name.like(f"%{search_query}%"))
            # 按科室过滤
            if selected_department:
                query = query.filter(Doctor.department_name == selected_department)

        doctors = query.all()  # 获取结果列表

        return render_template(
            'patient_appointment.html',
            doctors=doctors,
            department_list=department_list
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))


# 从数据库获取科室名称，按照拼音顺序返回
@app.route('/api/departments', methods=['GET'])
def get_departments():
    # 查询所有科室名称并去重
    departments = db.session.query(Doctor.department_name).distinct().order_by(Doctor.department_name).all()
    # 将结果转为列表
    department_list = [d.department_name for d in departments]
    return jsonify(department_list)


# 患者进行查找医生挂号
@app.route('/patient/register/<int:doctor_id>')
def register_doctor(doctor_id):
    if 'user_id' in session and session.get('role') == 'patient':
        doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
        if not doctor:
            flash('未找到该医生!', 'danger')
            return redirect(url_for('patient_appointment'))

        # 执行挂号操作（可在此处记录挂号信息，或进行进一步处理）
        flash(f'挂号成功！医生：{doctor.doctor_name}（{doctor.department_name}）', 'success')
        return redirect(url_for('patient_appointment'))
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))


# 患者查看个人处方
@app.route('/patient/prescriptions')
def patient_prescriptions():
    if 'user_id' in session and session.get('role') == 'patient':
        patient_id = session['related_id']  # 从 session 获取患者 ID
        prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()  # 查询患者的所有处方
        return render_template(
            'patient_prescriptions.html',
            prescriptions=prescriptions
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 患者查看个人处方详情
@app.route('/patient/prescription/<int:prescription_id>')
def prescription_detail(prescription_id):
    if 'user_id' in session and session.get('role') == 'patient':
        # 查询处方详细信息
        prescription = Prescription.query.filter_by(prescription_id=prescription_id).first()
        if not prescription:
            flash('未找到该处方的详细信息!', 'warning')
            return redirect(url_for('patient_prescriptions'))

        # 检查处方是否属于当前患者
        patient_id = session['related_id']
        if prescription.patient_id != patient_id:
            flash('您无权查看该处方!', 'danger')
            return redirect(url_for('patient_prescriptions'))

        # 查询患者姓名和医生姓名
        patient = Patient.query.filter_by(patient_id=prescription.patient_id).first()
        doctor = Doctor.query.filter_by(doctor_id=prescription.doctor_id).first()

        return render_template(
            'prescription_detail.html',
            prescription=prescription,
            patient_name=patient.patient_name if patient else "未知患者",
            doctor_name=doctor.doctor_name if doctor else "未知医生"
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 工人查看处方详情
@app.route('/worker/prescriptions')
def worker_prescriptions():
    if 'user_id' in session and session.get('role') == 'decoction_worker':
        username = session['username']
        # 查询分配给该工人的处方记录
        prescriptions = DecoctionRecord.query.filter(
            (DecoctionRecord.formulation_staff == username) |
            (DecoctionRecord.soaking_staff == username) |
            (DecoctionRecord.decoction_staff == username) |
            (DecoctionRecord.print_staff == username)
        ).all()

        return render_template(
            'worker_prescriptions.html',
            prescriptions=prescriptions
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 工人对处方进行操作
@app.route('/worker/prescription/<int:decoction_id>', methods=['GET', 'POST'])
def worker_prescription(decoction_id):
    if 'user_id' in session and session.get('role') == 'decoction_worker':
        decoction_record = DecoctionRecord.query.filter_by(decoction_id=decoction_id).first()

        if request.method == 'POST':
            action = request.form.get('action')
            username = session['username']

            if action == 'formulation':
                decoction_record.formulation_staff = username
                decoction_record.formulation_date = datetime.now()

            elif action == 'soaking':
                decoction_record.soaking_staff = username
                decoction_record.soaking_start_time = datetime.now()

            elif action == 'decoction':
                decoction_record.decoction_staff = username
                decoction_record.decoction_start_time = datetime.now()

            elif action == 'print':
                decoction_record.print_staff = username
                decoction_record.print_time = datetime.now()

            db.session.commit()
            flash('操作成功!', 'success')
            return redirect(url_for('worker_prescriptions'))

        return render_template(
            'worker_prescription.html',
            decoction_record=decoction_record
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 工厂管理员查询工人
@app.route('/factory/workers')
def view_workers():
    if 'user_id' in session and session.get('role') == 'decoction_worker' and session.get('is_factory_manager'):
        workers = User.query.filter_by(role='decoction_worker').all()  # 查询所有工人
        return render_template('view_workers.html', workers=workers)
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 工厂管理员查询订单
@app.route('/factory/orders')
def view_orders():
    if 'user_id' in session and session.get('role') == 'decoction_worker' and session.get('is_factory_manager'):
        orders = DecoctionRecord.query.all()  # 查询所有煎药订单
        return render_template('view_orders.html', orders=orders)
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))

# 工厂管理员分配任务
@app.route('/factory/assign_task', methods=['GET', 'POST'])
def assign_task():
    if 'user_id' in session and session.get('role') == 'decoction_worker' and session.get('is_factory_manager'):
        if request.method == 'POST':
            order_id = request.form.get('order_id')
            worker_id = request.form.get('worker_id')
            record = DecoctionRecord.query.filter_by(decoction_id=order_id).first()
            worker = User.query.filter_by(account_id=worker_id, role='decoction_worker').first()
            if record and worker:
                record.formulation_staff = worker.username
                db.session.commit()
                flash('任务分配成功!', 'success')
            else:
                flash('订单或工人不存在!', 'danger')
            return redirect(url_for('assign_task'))

        # 获取工人列表
        workers = User.query.filter_by(role='decoction_worker').all()
        # 获取所有未分配的订单
        orders = DecoctionRecord.query.filter(DecoctionRecord.formulation_staff == None).all()
        # 获取已分配的任务
        assigned_tasks = DecoctionRecord.query.filter(DecoctionRecord.formulation_staff != None).all()

        return render_template(
            'assign_task.html',
            workers=workers,
            orders=orders,
            assigned_tasks=assigned_tasks  # 将已分配任务传递给前端
        )
    else:
        flash('您没有权限访问此页面!', 'warning')
        return redirect(url_for('home'))




# 启动应用
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保数据库结构同步
    app.run(debug=True)
