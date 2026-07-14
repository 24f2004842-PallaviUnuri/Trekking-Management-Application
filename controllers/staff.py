from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User, Trek, Booking
from flask_login import login_required, current_user
from datetime import date,datetime
from sqlalchemy import func,extract
from functools import wraps

def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'staff':
            flash('Staff access only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

staff_bp = Blueprint('staff',__name__)

@staff_bp.route('/dashboard',methods=['GET','POST'])
@login_required
@staff_required
def dashboard():
    my_treks = Trek.query.filter_by(assigned_staff_id = current_user.id).all()
    total_assigned = len(my_treks)
    total_open = len([t for t in my_treks if t.status == "Open"])
    # total_participants = len()
    
    upcoming_treks = Trek.query.filter(Trek.assigned_staff_id == current_user.id,
                                       Trek.start_date >= date.today()).order_by(Trek.start_date.asc()).first()
    
    my_trek = Trek.query.filter_by(assigned_staff_id = current_user.id).all()
    total_participants = (
        db.session.query(func.count(Booking.id))
    .join(Trek, Booking.trek_id == Trek.id)
    .filter(Trek.assigned_staff_id == current_user.id)
    .filter(Booking.status.in_(['Booked', 'Completed']))
    .scalar() or 0)
    
    return render_template('staff/staff_dashboard.html',my_treks = my_treks,total_assigned=total_assigned,
                           total_open=total_open,my_trek=my_trek,
                           upcoming_treks=upcoming_treks,
                           total_participants=total_participants)
    

@staff_bp.route('/my_trek')
@login_required
@staff_required
def my_trek():
    my_trek = Trek.query.filter_by(assigned_staff_id = current_user.id).all()
    return render_template('staff/my_trek.html', my_trek = my_trek)

@staff_bp.route('/manage_trek/<int:trek_id>',methods = ['GET','POST'])
@login_required
@staff_required
def manage_trek(trek_id):
    
    current_trek = Trek.query.get_or_404(trek_id)
    if current_user.id != current_trek.assigned_staff_id:
        flash("Access Denied",'danger')
        return redirect(url_for('staff.dashboard'))
        
    if request.method == "POST":
        available_slots = request.form.get("available_slots")
        status = request.form.get("status")
        current_trek.available_slots = available_slots
        current_trek.status = status
        db.session.commit()
        flash("Updated Successfully.",'success')
    
    return render_template('staff/staff_manage_trek.html', trek=current_trek)

@staff_bp.route('/profile',methods=['GET','POST'])
@login_required
@staff_required
def edit_profile():
    profile = User.query.filter_by(role='staff',id = current_user.id).first_or_404()
    if request.method == "POST":
        name=request.form.get('name')
        phone_no=request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        blood_group = request.form.get('blood_group')
        address = request.form.get('address')
        
        profile.name = name
        profile.phone = phone_no
        profile.dob = datetime.strptime(dob,'%Y-%m-%d').date()
        profile.gender = gender
        profile.blood_group = blood_group
        profile.address = address
        
        db.session.commit()
        flash("Profile Updated",'success')
    return render_template('staff/my_profile.html',profile=profile)

@staff_bp.route('/participants/<int:trek_id>')
@login_required
@staff_required
def participants(trek_id):
    trek = db.session.get(Trek,trek_id)
    if not trek or current_user.id != trek.assigned_staff_id:
        flash("Access Denied", "danger")
        return redirect(url_for('staff.dashboard'))
    #start with query
    query = db.session.query(Booking,User)
    #join the user table based on userid of booking table
    query = query.join(User, Booking.user_id == User.id)
    # filter by trek_id
    query = query.filter(Booking.trek_id == trek_id,Booking.status!= "Cancelled")
    participants = query.all()
    return render_template('staff/trek_participants.html',
                           participants=participants,trek=trek)