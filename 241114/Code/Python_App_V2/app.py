from flask import Flask, render_template, request, redirect, url_for, session, flash , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# 初始化应用
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 配置 SQL Server 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://sa:20050317@localhost/SDDB?driver=ODBC+Driver+17+for+SQL+Server'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer)

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact_number = db.Column(db.String(15))

class Doctor(db.Model):
    __tablename__ = 'doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    department = db.Column(db.String(50))
    title = db.Column(db.String(50))
    contact_number = db.Column(db.String(15))

class Worker(db.Model):
    __tablename__ = 'workers'
    worker_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    contact_number = db.Column(db.String(15))

class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15))

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    prescription_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)
    usage_instructions = db.Column(db.Text)
    status = db.Column(db.String(20), default='待配方')
    expected_pickup_time = db.Column(db.DateTime)

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'))
    receive_worker_id = db.Column(db.Integer, db.ForeignKey('workers.worker_id'))
    receive_worker_name = db.Column(db.String(50))
    form_worker_id = db.Column(db.Integer, db.ForeignKey('workers.worker_id'))
    form_worker_name = db.Column(db.String(50))
    decoction_worker_id = db.Column(db.Integer, db.ForeignKey('workers.worker_id'))
    decoction_worker_name = db.Column(db.String(50))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'))
    admin_name = db.Column(db.String(50))
    receive_time = db.Column(db.DateTime)
    form_time = db.Column(db.DateTime)
    decoction_start_time = db.Column(db.DateTime)
    decoction_end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='未完成')

# 首页
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# 登录模块
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user:  # 用户验证成功
            session['user_id'] = user.uuid
            session['role'] = user.role
            session['username'] = user.username

            # 根据角色设置角色相关的 session 信息
            if user.role == 'patient':
                patient = Patient.query.filter_by(patient_id=user.role_id).first()
                session['name'] = patient.name if patient else '未知患者'
                session['role_id'] = user.role_id  # 存储患者 ID
            elif user.role == 'doctor':
                doctor = Doctor.query.filter_by(doctor_id=user.role_id).first()
                session['name'] = doctor.name if doctor else '未知医生'
                session['role_id'] = user.role_id  # 存储医生 ID
            elif user.role == 'worker':
                worker = Worker.query.filter_by(worker_id=user.role_id).first()
                session['name'] = worker.name if worker else '未知工人'
                session['role_id'] = user.role_id  # 存储工人 ID
            elif user.role == 'admin':
                admin = Admin.query.filter_by(admin_id=user.role_id).first()
                session['name'] = admin.name if admin else '未知管理员'
                session['role_id'] = user.role_id  # 存储管理员 ID

            flash('登录成功!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误!', 'danger')
    return render_template('login.html')

# 注册模块
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        password = request.form.get('password', '123456')  # 默认密码
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        contact_number = request.form.get('contact_number')

        # 验证角色（只能是患者）
        role = 'patient'

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(f"用户名 {username} 已存在，请选择其他用户名!", 'danger')
            return redirect(url_for('register'))

        # 创建患者信息
        try:
            new_patient = Patient(name=name, gender=gender, age=age, contact_number=contact_number)
            db.session.add(new_patient)
            db.session.flush()  # 获取生成的 patient_id
            role_id = new_patient.patient_id

            # 创建用户（仅患者角色）
            new_user = User(username=username, password=password, role=role, role_id=role_id)
            db.session.add(new_user)
            db.session.commit()

            flash(f"用户 {username} 注册成功! UUID: {new_user.uuid}, 角色: {role}, 角色ID: {role_id}", 'success')
            return redirect(url_for('login'))  # 注册成功后重定向到登录页面

        except Exception as e:
            db.session.rollback()
            flash(f"注册失败: {str(e)}", 'danger')
    return render_template('register.html')

# 注销模块
@app.route('/logout')
def logout():
    session.clear()
    # flash('已注销!', 'info')
    flash(' ', 'info')
    return redirect(url_for('login'))

# 通用仪表盘
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', role=session.get('role'))

# 管理员查看个人信息
@app.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    if 'user_id' in session and session.get('role') == 'admin':
        admin_id = session.get('role_id')  # 获取管理员的 role_id
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        if request.method == 'POST':
            # 修改管理员信息
            new_name = request.form.get('name')
            new_contact = request.form.get('contact_number')
            if admin:
                admin.name = new_name
                admin.contact_number = new_contact
                db.session.commit()
                flash('个人信息更新成功!', 'success')
                return redirect(url_for('admin_profile'))
            flash('管理员信息更新失败!', 'danger')

        if admin:
            return render_template('admin_profile.html', admin=admin)
        flash('管理员信息未找到!', 'danger')
        return redirect(url_for('dashboard'))
    flash('无权限访问!', 'danger')
    return redirect(url_for('login'))

# 用户管理/添加用户
@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if 'user_id' in session and session.get('role') == 'admin':
        selected_role = request.args.get('role', 'all')  # 获取筛选的角色，默认为 'all'
        search_username = request.args.get('username', '').strip()  # 获取搜索用户名，默认为空字符串
        page = int(request.args.get('page', 1))  # 获取当前页数，默认为第 1 页
        per_page = 10  # 每页显示用户数量

        if request.method == 'POST':
            # 添加新用户
            username = request.form.get('username')
            password = request.form.get('password', '123456')  # 默认密码
            role = request.form.get('role')

            try:
                if role == 'patient':
                    name = request.form.get('name')
                    gender = request.form.get('gender')
                    age = request.form.get('age')
                    contact_number = request.form.get('contact_number')
                    new_patient = Patient(name=name, gender=gender, age=age, contact_number=contact_number)
                    db.session.add(new_patient)
                    db.session.flush()  # 获取生成的 patient_id
                    role_id = new_patient.patient_id

                elif role == 'worker':
                    name = request.form.get('name')
                    age = request.form.get('age')
                    contact_number = request.form.get('contact_number')
                    new_worker = Worker(name=name, age=age, contact_number=contact_number)
                    db.session.add(new_worker)
                    db.session.flush()  # 获取生成的 worker_id
                    role_id = new_worker.worker_id

                elif role == 'admin':
                    name = request.form.get('name')
                    contact_number = request.form.get('contact_number')
                    new_admin = Admin(name=name, contact_number=contact_number)
                    db.session.add(new_admin)
                    db.session.flush()  # 获取生成的 admin_id
                    role_id = new_admin.admin_id

                else:
                    flash('角色类型错误!', 'danger')
                    return redirect(url_for('admin_users'))

                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    flash(f"用户名 {username} 已存在，请选择其他用户名!", 'danger')
                    return redirect(url_for('admin_users'))

                new_user = User(username=username, password=password, role=role, role_id=role_id)
                db.session.add(new_user)
                db.session.commit()
                flash(f"用户 {username} 添加成功! UUID: {new_user.uuid}, 角色: {role}, 角色ID: {role_id}", 'success')

            except Exception as e:
                db.session.rollback()
                flash(f"添加用户失败: {str(e)}", 'danger')

        # 构建查询语句
        query = User.query

        # 按角色筛选
        if selected_role != 'all':
            query = query.filter_by(role=selected_role)

        # 按用户名模糊搜索
        if search_username:
            query = query.filter(User.username.like(f"%{search_username}%"))

        # 获取总用户数
        total_users = query.count()

        # 分页处理
        users = query.order_by(User.role, User.role_id).offset((page - 1) * per_page).limit(per_page).all()
        total_pages = (total_users + per_page - 1) // per_page  # 计算总页数

        return render_template(
            'admin_users.html',
            users=users,
            selected_role=selected_role,
            search_username=search_username,
            current_page=page,
            total_pages=total_pages,  # 传递总页数到前端
        )
    else:
        flash('无权限访问!', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/admin/users/delete/<uuid>', methods=['POST'])
def delete_user(uuid):
    if 'user_id' in session and session.get('role') == 'admin':
        try:
            # 获取要删除的用户
            user = User.query.filter_by(uuid=uuid).first()
            if user:
                role = user.role
                role_id = user.role_id

                # 根据角色删除相应角色表数据
                if role == 'patient':
                    patient = Patient.query.filter_by(patient_id=role_id).first()
                    if patient:
                        db.session.delete(patient)
                elif role == 'worker':
                    worker = Worker.query.filter_by(worker_id=role_id).first()
                    if worker:
                        db.session.delete(worker)
                elif role == 'admin':
                    admin = Admin.query.filter_by(admin_id=role_id).first()
                    if admin:
                        db.session.delete(admin)

                # 删除用户
                db.session.delete(user)
                db.session.commit()
                flash(f"用户 {user.username} 已成功删除", 'success')
            else:
                flash("未找到用户", 'danger')

        except Exception as e:
            db.session.rollback()
            flash(f"删除失败: {str(e)}", 'danger')

    return redirect(url_for('admin_users'))


# 用户名查重
@app.route('/admin/users/validate_username', methods=['GET'])
def validate_username():
    username = request.args.get('username')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'valid': False, 'message': f"用户名 {username} 已存在"}
    return {'valid': True, 'message': f"用户名 {username} 可用"}



# 编辑用户
@app.route('/admin/users/edit/<uuid>', methods=['GET', 'POST'])
def edit_user(uuid):
    if 'user_id' in session and session.get('role') == 'admin':
        user = User.query.get_or_404(uuid)

        # 获取具体角色的信息
        patient = Patient.query.filter_by(patient_id=user.role_id).first() if user.role == 'patient' else None
        doctor = Doctor.query.filter_by(doctor_id=user.role_id).first() if user.role == 'doctor' else None
        worker = Worker.query.filter_by(worker_id=user.role_id).first() if user.role == 'worker' else None
        admin = Admin.query.filter_by(admin_id=user.role_id).first() if user.role == 'admin' else None

        if request.method == 'POST':
            # 修改用户信息
            user.username = request.form.get('username', user.username)
            user.password = request.form.get('password', user.password)

            # 修改对应角色信息
            if user.role == 'patient' and patient:
                patient.name = request.form.get('patient_name', patient.name)
                patient.gender = request.form.get('patient_gender', patient.gender)
                patient.age = request.form.get('patient_age', patient.age)
                patient.contact_number = request.form.get('patient_contact', patient.contact_number)
            elif user.role == 'doctor' and doctor:
                doctor.name = request.form.get('doctor_name', doctor.name)
                doctor.gender = request.form.get('doctor_gender', doctor.gender)
                doctor.department = request.form.get('doctor_department', doctor.department)
                doctor.title = request.form.get('doctor_title', doctor.title)
                doctor.contact_number = request.form.get('doctor_contact', doctor.contact_number)
            elif user.role == 'worker' and worker:
                worker.name = request.form.get('worker_name', worker.name)
                worker.age = request.form.get('worker_age', worker.age)
                worker.contact_number = request.form.get('worker_contact', worker.contact_number)
            elif user.role == 'admin' and admin:
                admin.name = request.form.get('admin_name', admin.name)
                admin.contact_number = request.form.get('admin_contact', admin.contact_number)

            db.session.commit()
            flash(f"用户 {user.username} 更新成功!", 'success')
            return redirect(url_for('admin_users'))

        return render_template('edit_user.html', user=user, patient=patient, doctor=doctor, worker=worker, admin=admin)
    else:
        flash('无权限访问!', 'danger')
        return redirect(url_for('dashboard'))


# # 删除用户
# @app.route('/admin/users/delete/<uuid>', methods=['POST'])
# def delete_user(uuid):
#     if 'user_id' in session and session.get('role') == 'admin':
#         user = User.query.get_or_404(uuid)
#         db.session.delete(user)
#         db.session.commit()
#         flash(f"用户 {user.username} 删除成功!", 'success')
#         return redirect(url_for('admin_users'))
#     else:
#         flash('无权限访问!', 'danger')
#         return redirect(url_for('dashboard'))

# 分配任务
from flask import jsonify

@app.route('/admin/assign_tasks', methods=['GET', 'POST'])
def assign_tasks():
    if 'user_id' in session and session.get('role') == 'admin':
        if request.method == 'POST':
            task_id = request.form.get('task_id')
            operation = request.form.get('operation')  # 'assign' or 'rollback'
            print(f"Received operation: {operation} for task_id: {task_id}")

            if operation == 'assign':
                worker_id = int(request.form.get('worker_id'))
                task_type = request.form.get('task_type')  # 'receive', 'formulate', 'decoction'

                # 获取任务和工人信息
                task = Task.query.get_or_404(task_id)
                worker = Worker.query.get_or_404(worker_id)

                # 检查任务分配规则
                print(f"Assigning task {task_id} to worker {worker_id} for task type {task_type}")

                if task_type == 'formulate' and not task.receive_time:
                    print("Error: Receive step not completed")
                    return jsonify({'success': False, 'message': '必须完成收方后才能分配配方任务!'})

                if task_type == 'decoction' and not task.form_time:
                    print("Error: Formulate step not completed")
                    return jsonify({'success': False, 'message': '必须完成配方后才能分配煎药任务!'})

                # 分配任务
                if task_type == 'receive':
                    task.receive_worker_id = worker_id
                    task.receive_worker_name = worker.name
                elif task_type == 'formulate':
                    task.form_worker_id = worker_id
                    task.form_worker_name = worker.name
                elif task_type == 'decoction':
                    task.decoction_worker_id = worker_id
                    task.decoction_worker_name = worker.name

                db.session.commit()
                print(f"Task {task_id} successfully assigned to {worker.name}")
                return jsonify({'success': True, 'message': f'任务 {task_id} 成功分配给工人 {worker.name}!'})

            elif operation == 'rollback':
                rollback_password = request.form.get('rollback_password')
                admin_user = User.query.filter_by(uuid=session['user_id']).first()

                if not admin_user or admin_user.password != rollback_password:
                    return jsonify({'success': False, 'message': '操作密码错误! 无法执行回退操作。'})

                task = Task.query.get_or_404(task_id)

                # 获取回退阶段
                rollback_phase = request.form.get('rollback_phase')

                # 回退逻辑
                if rollback_phase == 'receive' and task.receive_time:
                    task.receive_time = None
                    task.receive_worker_id = None
                    task.receive_worker_name = None
                    task.status = '未完成'  # 状态变为未完成
                    db.session.commit()
                    return jsonify({'success': True, 'message': f"任务 {task_id} 已成功回退到收方前!"})

                elif rollback_phase == 'formulate' and task.form_time:
                    task.form_time = None
                    task.form_worker_id = None
                    task.form_worker_name = None
                    db.session.commit()
                    return jsonify({'success': True, 'message': f"任务 {task_id} 已成功回退到配方前!"})

                # 检查并回退到其他阶段
                # ... (同样的逻辑可以应用于其他阶段)

                else:
                    return jsonify({'success': False, 'message': '无法回退到该阶段。'})

        # 查询任务统计信息
        unfinished_tasks = Task.query.filter(Task.status != '完成').count()
        finished_tasks = Task.query.filter(Task.status == '完成').count()

        stats = {'unfinished_orders': unfinished_tasks, 'finished_orders': finished_tasks}

        tasks = Task.query.order_by(Task.status.desc(), Task.task_id.asc()).all()
        for task in tasks:
            if task.decoction_end_time:
                task.phase_status = "煎药已完成"
            elif task.decoction_start_time:
                task.phase_status = "煎药进行中"
            elif task.form_time:
                task.phase_status = "配方已完成，煎药未完成"
            elif task.receive_time:
                task.phase_status = "收方已完成，配方未完成"
            else:
                task.phase_status = "收方未完成"

        workers = Worker.query.all()
        return render_template('assign_tasks.html', tasks=tasks, workers=workers, stats=stats)

    flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))


# 医生个人信息页面
@app.route('/doctor/profile', methods=['GET', 'POST'])
def doctor_profile():
    if 'user_id' in session and session.get('role') == 'doctor':
        doctor_id = session.get('role_id')
        doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
        doctor_user = User.query.filter_by(role_id=doctor_id, role='doctor').first()

        if request.method == 'POST':
            # 更新信息
            doctor.name = request.form.get('name')
            doctor.gender = request.form.get('gender')
            doctor.department = request.form.get('department')
            doctor.title = request.form.get('title')
            doctor.contact_number = request.form.get('contact_number')

            # 更新医生 ID
            department_code = {'内科': '01', '外科': '02', '儿科': '03', '妇科': '04'}.get(doctor.department, '00')
            title_code = {'主任医师': '01', '副主任医师': '02', '主治医师': '03', '住院医师': '04'}.get(doctor.title, '00')
            doctor_id_suffix = str(doctor.doctor_id)[-4:]  # 保留原 ID 的后四位
            doctor.doctor_id = int(department_code + title_code + doctor_id_suffix)

            db.session.commit()

            # 提示信息
            flash(
                f"信息更新成功! 新医生 ID: {doctor.doctor_id}, UUID: {doctor_user.uuid}, 姓名: {doctor.name}, 科室: {doctor.department}, 职称: {doctor.title}",
                'success'
            )
            return redirect(url_for('doctor_profile'))

        return render_template('doctor_profile.html', doctor=doctor, doctor_user=doctor_user)
    else:
        flash('无权限访问!', 'danger')
        return redirect(url_for('dashboard'))




# 医生开处方
@app.route('/doctor/prescriptions/new', methods=['GET', 'POST'])
def create_prescription():
    if 'user_id' in session and session.get('role') == 'doctor':
        doctor_id = session.get('role_id')  # 使用 role_id 确保匹配 doctor_id

        if request.method == 'POST':
            # 获取表单数据
            patient_id = request.form.get('patient_id')
            amount = request.form.get('amount')
            usage_instructions = request.form.get('usage_instructions')

            # 创建新处方
            new_prescription = Prescription(
                patient_id=patient_id,
                doctor_id=doctor_id,
                amount=amount,
                usage_instructions=usage_instructions,
                status='待配方'  # 默认状态
            )
            db.session.add(new_prescription)
            db.session.commit()  # 这里提交事务，生成处方ID

            # 获取新生成的处方ID
            prescription_id = new_prescription.prescription_id

            # 创建新任务，仅填写处方id，其他为空
            new_task = Task(
                prescription_id=prescription_id,
                receive_worker_id=None,
                receive_worker_name=None,
                form_worker_id=None,
                form_worker_name=None,
                decoction_worker_id=None,
                decoction_worker_name=None,
                admin_id=None,
                admin_name=None,
                receive_time=None,
                form_time=None,
                decoction_start_time=None,
                decoction_end_time=None,
                status='未完成'  # 默认任务状态
            )
            db.session.add(new_task)
            db.session.commit()  # 提交任务数据

            flash('处方创建成功，并已生成任务!', 'success')
            return redirect(url_for('doctor_prescriptions'))

        # 获取所有患者信息（供下拉选择患者）
        patients = Patient.query.all()
        return render_template('create_prescription.html', patients=patients)

    else:
        flash('无权限访问!', 'danger')
        return redirect(url_for('dashboard'))



# 医生查看处方
@app.route('/doctor/prescriptions')
def doctor_prescriptions():
    if 'user_id' in session and session.get('role') == 'doctor':
        doctor_id = session.get('role_id')  # 使用 role_id 进行匹配
        if doctor_id:
            prescriptions = Prescription.query.filter_by(doctor_id=doctor_id).all()
            prescriptions_with_status = []
            for prescription in prescriptions:
                task = Task.query.filter_by(prescription_id=prescription.prescription_id).first()
                if not task:
                    status = "未分配任务"
                elif not task.receive_time:
                    status = "待收方"
                elif not task.form_time:
                    status = "待配方"
                elif not task.decoction_start_time:
                    status = "待煎药"
                elif not task.decoction_end_time:
                    status = "煎药中"
                else:
                    status = "已完成"
                prescriptions_with_status.append({
                    "prescription": prescription,
                    "status": status
                })
            return render_template('doctor_prescriptions.html', prescriptions=prescriptions_with_status)
        flash('未找到医生信息!', 'danger')
    else:
        flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))


# 医生查看处方详情
@app.route('/doctor/prescriptions/view/<int:prescription_id>', methods=['GET'])
def doctor_prescription_detail(prescription_id):
    if 'user_id' in session and session.get('role') == 'doctor':
        # 获取医生 ID 并验证
        doctor_id = session.get('role_id')
        prescription = Prescription.query.filter_by(prescription_id=prescription_id, doctor_id=doctor_id).first()
        if prescription:
            # 查询任务信息
            task = Task.query.filter_by(prescription_id=prescription_id).first()
            return render_template('doctor_prescription_detail.html', prescription=prescription, task=task)
        flash('未找到该处方或无权限查看!', 'danger')
        return redirect(url_for('doctor_prescriptions'))
    flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))

# 患者个人信息
@app.route('/patient/profile', methods=['GET', 'POST'])
def patient_profile():
    if 'user_id' in session and session.get('role') == 'patient':
        patient_id = session.get('role_id')
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        patient_user = User.query.filter_by(role_id=patient_id, role='patient').first()

        if request.method == 'POST':
            # 更新信息
            patient.name = request.form.get('name')
            patient.gender = request.form.get('gender')
            patient.age = request.form.get('age')
            patient.contact_number = request.form.get('contact_number')

            db.session.commit()

            # 提示信息
            flash(
                f"信息更新成功! 患者 ID: {patient.patient_id}, UUID: {patient_user.uuid}, 姓名: {patient.name}, 年龄: {patient.age}",
                'success'
            )
            return redirect(url_for('patient_profile'))

        return render_template('patient_profile.html', patient=patient, patient_user=patient_user)
    else:
        flash('无权限访问!', 'danger')
        return redirect(url_for('dashboard'))


# 患者查看处方
@app.route('/patient/prescriptions', methods=['GET'])
def patient_prescriptions():
    if 'user_id' in session and session.get('role') == 'patient':
        patient_id = session.get('role_id')  # role_id 对应 patient_id
        if patient_id:
            prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
            prescriptions_with_status = []
            for prescription in prescriptions:
                task = Task.query.filter_by(prescription_id=prescription.prescription_id).first()
                if not task:
                    status = "未分配任务"
                elif not task.receive_time:
                    status = "待收方"
                elif not task.form_time:
                    status = "待配方"
                elif not task.decoction_start_time:
                    status = "待煎药"
                elif not task.decoction_end_time:
                    status = "煎药中"
                else:
                    status = "已完成"
                prescriptions_with_status.append({
                    "prescription": prescription,
                    "status": status
                })
            return render_template('patient_prescriptions.html', prescriptions=prescriptions_with_status)
        flash('未找到患者信息!', 'danger')
    else:
        flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))


# 患者查看处方详情
@app.route('/patient/prescriptions/view/<int:prescription_id>', methods=['GET'])
def patient_prescription_detail(prescription_id):
    if 'user_id' in session and session.get('role') == 'patient':
        # 获取患者 ID 并验证
        patient_id = session.get('role_id')
        prescription = Prescription.query.filter_by(prescription_id=prescription_id, patient_id=patient_id).first()
        if prescription:
            # 查询任务信息
            task = Task.query.filter_by(prescription_id=prescription_id).first()
            return render_template('patient_prescription_detail.html', prescription=prescription, task=task)
        flash('未找到该处方或无权限查看!', 'danger')
        return redirect(url_for('patient_prescriptions'))
    flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))

# 工人个人信息
@app.route('/worker/profile', methods=['GET'])
def worker_profile():
    if 'user_id' in session and session.get('role') == 'worker':
        # 获取工人 ID 并查询信息
        worker_id = session.get('role_id')
        worker = Worker.query.filter_by(worker_id=worker_id).first()
        if worker:
            return render_template('worker_profile.html', worker=worker)
        flash('未找到工人信息!', 'danger')
        return redirect(url_for('dashboard'))
    flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))


# 工作人员查看任务
@app.route('/worker/tasks', methods=['GET'])
def worker_tasks():
    if 'user_id' in session and session.get('role') == 'worker':
        worker_id = int(session.get('role_id'))
        tasks = Task.query.filter(
            (Task.receive_worker_id == worker_id) |
            (Task.form_worker_id == worker_id) |
            (Task.decoction_worker_id == worker_id)
        ).all()
        return render_template('worker_tasks.html', tasks=tasks)

    flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))



# 工作人员更新任务状态
@app.route('/worker/tasks/update/<int:task_id>', methods=['GET', 'POST'])
def update_task_status(task_id):
    if 'user_id' in session and session.get('role') == 'worker':
        worker_id = int(session.get('role_id'))  # 当前工人 ID
        task = Task.query.get_or_404(task_id)

        # 如果任务已完成，直接跳回任务列表
        if task.status == '完成':
            flash('任务已完成，无法继续更新状态!', 'info')
            return redirect(url_for('worker_tasks'))

        # 验证任务是否分配给当前工人
        if task.receive_worker_id != worker_id and task.form_worker_id != worker_id and task.decoction_worker_id != worker_id:
            flash('无权限操作此任务!', 'danger')
            return redirect(url_for('worker_tasks'))

        if request.method == 'POST':
            action = request.form.get('action')

            # 更新任务状态逻辑
            if action == 'receive' and task.receive_worker_id == worker_id and not task.receive_time:
                task.receive_time = datetime.utcnow()
            elif action == 'formulate' and task.form_worker_id == worker_id and task.receive_time and not task.form_time:
                task.form_time = datetime.utcnow()
            elif action == 'decoction_start' and task.decoction_worker_id == worker_id and task.form_time and not task.decoction_start_time:
                task.decoction_start_time = datetime.utcnow()
            elif action == 'decoction_end' and task.decoction_worker_id == worker_id and task.decoction_start_time and not task.decoction_end_time:
                task.decoction_end_time = datetime.utcnow()
                task.status = '完成'
            else:
                flash('当前任务未满足操作条件，无法完成此操作。', 'warning')
                return redirect(url_for('update_task_status', task_id=task_id))

            db.session.commit()
            flash('任务状态更新成功!', 'success')
            return redirect(url_for('worker_tasks'))

        return render_template('update_task.html', task=task)

    flash('无权限访问!', 'danger')
    return redirect(url_for('dashboard'))
#
# # 个人信息页面聚合
# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     if 'user_id' not in session:
#         flash('请先登录!', 'danger')
#         return redirect(url_for('login'))
#
#     user_role = session.get('role')
#     role_id = session.get('role_id')
#
#     # 根据角色获取用户信息
#     user_data = None
#     if user_role == 'admin':
#         user_data = Admin.query.filter_by(admin_id=role_id).first()
#     elif user_role == 'doctor':
#         user_data = Doctor.query.filter_by(doctor_id=role_id).first()
#     elif user_role == 'patient':
#         user_data = Patient.query.filter_by(patient_id=role_id).first()
#     elif user_role == 'worker':
#         user_data = Worker.query.filter_by(worker_id=role_id).first()
#
#     if not user_data:
#         flash('未找到用户信息!', 'danger')
#         return redirect(url_for('dashboard'))
#
#     if request.method == 'POST':
#         # 更新信息
#         if user_role == 'admin':
#             user_data.name = request.form.get('name')
#             user_data.contact_number = request.form.get('contact_number')
#         elif user_role == 'doctor':
#             user_data.name = request.form.get('name')
#             user_data.gender = request.form.get('gender')
#             user_data.department = request.form.get('department')
#             user_data.title = request.form.get('title')
#             user_data.contact_number = request.form.get('contact_number')
#
#             # 自动生成新的 doctor_id
#             department_code = {'内科': '01', '外科': '02', '儿科': '03', '妇科': '04'}.get(user_data.department, '00')
#             title_code = {'主任医师': '01', '副主任医师': '02', '主治医师': '03', '住院医师': '04'}.get(user_data.title, '00')
#             doctor_id_suffix = str(user_data.doctor_id)[-4:]  # 保留原 ID 的后四位
#             user_data.doctor_id = int(department_code + title_code + doctor_id_suffix)
#         elif user_role == 'patient':
#             user_data.name = request.form.get('name')
#             user_data.gender = request.form.get('gender')
#             user_data.age = request.form.get('age')
#             user_data.contact_number = request.form.get('contact_number')
#         elif user_role == 'worker':
#             # 工人信息不允许修改
#             flash('工人信息不可修改!', 'warning')
#             return redirect(url_for('profile'))
#
#         try:
#             db.session.commit()
#             flash(f"信息更新成功!", 'success')
#         except Exception as e:
#             db.session.rollback()
#             flash(f"信息更新失败: {str(e)}", 'danger')
#
#         return redirect(url_for('profile'))
#
#     # 渲染页面
#     return render_template('profile.html', user_data=user_data)




# 初始化数据库
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建所有表
    app.run(debug=True)
