from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User
from flask_login import login_user, logout_user, login_required 
from werkzeug.security import generate_password_hash, check_password_hash 

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register',methods=['GET', 'POST'])
def register():
    if request.method =='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        if password != confirm_password:
            flash("Password do no match.",'danger')
            return redirect(url_for('auth.register'))
        if role == "trekker":
            new_user = User(
                name=name,
                email=email,
                status='Active',
                password=password,
                role = "trekker"
            )
            db.session.add(new_user)
        else:
            new_staff = User(
                name=name,
                email=email,
                status='Pending',
                password=password,
                role = "staff"
            )
            
            db.session.add(new_staff)   
        
        db.session.commit()
        
            
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        

        if not user:
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))

        login_user(user) 
        
        if user.role == "admin":
            return redirect(url_for('admin.dashboard'))
        elif user.role == "staff":
            
            if (user and user.status == "Approved"):
                return redirect(url_for('staff.dashboard'))
            flash("Your Staff Profile is awaiting Admin approval.",'warning')
            logout_user()
        else:
            return redirect(url_for('trekker.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required 
def logout():
    logout_user()
    flash("Logged out successfully.",'success')
    return redirect(url_for('auth.login'))
    