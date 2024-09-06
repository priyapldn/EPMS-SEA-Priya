from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm
from app.models import Employee
from app.database import get_session

auth = Blueprint('auth', __name__)

@auth.route("/")
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        session = get_session()
        employee_exists = session.query(Employee).filter_by(username=username).first()

        if employee_exists and check_password_hash(employee_exists.password, password):
            login_user(employee_exists, remember=remember)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password. Please try again', 'danger')
    
    return render_template('login.html', form=form)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    session = get_session()

    name = request.form.get('name')
    employee_number = request.form.get('employee_number')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    existing_employee = session.query(Employee).filter_by(email=email).first()

    if existing_employee:
        flash('Email address already exists.')
        return redirect(url_for('auth.register'))

    new_employee = Employee(name=name, employee_number=employee_number,email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), is_admin=False)
    
    session.add(new_employee)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))