from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# 初始化 Flask 应用
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 替换为更安全的密钥

# 配置 SQL Server 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://sa:20050317@localhost/DecoctionSystem?driver=ODBC+Driver+17+for+SQL+Server'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# 首页
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session.get('username'))
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
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
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
        prescriptions = db.session.execute(text('SELECT * FROM Prescriptions')).fetchall()
        decoction_records = db.session.execute(text('SELECT * FROM DecoctionRecords')).fetchall()
        return render_template(
            'admin_all.html',
            users=users,
            patients=patients,
            prescriptions=prescriptions,
            decoction_records=decoction_records
        )
    else:
        flash('您没有权限查看此页面!', 'warning')
        return redirect(url_for('home'))


# 医生查看患者及相关信息
@app.route('/doctor/patients')
def doctor_patients():
    if 'user_id' in session and session.get('role') == 'doctor':
        doctor_id = session['user_id']
        patients = db.session.execute(
            text('''
            SELECT DISTINCT p.*
            FROM Patients p
            JOIN Prescriptions ps ON p.patient_id = ps.patient_id
            WHERE ps.doctor_id = :doctor_id
            '''),
            {'doctor_id': doctor_id}
        ).fetchall()
        prescriptions = db.session.execute(
            text('SELECT * FROM Prescriptions WHERE doctor_id = :doctor_id'),
            {'doctor_id': doctor_id}
        ).fetchall()
        decoction_records = db.session.execute(
            text('''
            SELECT dr.*
            FROM DecoctionRecords dr
            JOIN Prescriptions ps ON dr.prescription_id = ps.prescription_id
            WHERE ps.doctor_id = :doctor_id
            '''),
            {'doctor_id': doctor_id}
        ).fetchall()
        return render_template(
            'doctor_patients.html',
            patients=patients,
            prescriptions=prescriptions,
            decoction_records=decoction_records
        )
    else:
        flash('您没有权限查看此页面!', 'warning')
        return redirect(url_for('home'))


# 患者查看个人信息和处方
@app.route('/patient/info')
def patient_info():
    if 'user_id' in session and session.get('role') == 'patient':
        patient_id = session['user_id']
        personal_info = db.session.execute(
            text('SELECT * FROM Patients WHERE patient_id = :patient_id'),
            {'patient_id': patient_id}
        ).fetchone()
        prescriptions = db.session.execute(
            text('SELECT * FROM Prescriptions WHERE patient_id = :patient_id'),
            {'patient_id': patient_id}
        ).fetchall()
        return render_template(
            'patient_info.html',
            personal_info=personal_info,
            prescriptions=prescriptions
        )
    else:
        flash('您没有权限查看此页面!', 'warning')
        return redirect(url_for('home'))


# 启动应用
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
