from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User, Trek, Booking
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime,date

admin_bp = Blueprint('admin',__name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    total_treks = Trek.query.count()
    total_staff = User.query.filter_by(role='staff',status='Active').count()
    total_trekkers = User.query.filter_by(role='trekker',status='Active').count()
    total_bookings = Booking.query.count()
    
    recent_treks = Trek.query.order_by(Trek.id.desc()).limit(5).all()
    recent_bookings =Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    upcoming_treks =Trek.query.filter(Trek.start_date >= date.today()).order_by(Trek.start_date.asc()).limit(3).all()

    return render_template('admin/admin_dashboard.html',
                           total_treks=total_treks,
                           total_staff = total_staff,
                           total_bookings=total_bookings,
                           total_trekkers=total_trekkers,
                           recent_treks=recent_treks,
                           recent_bookings=recent_bookings,
                            upcoming_treks=upcoming_treks)

@admin_bp.route('/treks')
def manage_treks():
    query = Trek.query
    query = query.join(Booking.trek)
    #search for booked trek page
    search = request.args.get('search')
    difficulty = request.args.get('difficulty')
    duration = request.args.get('duration')
    if search:
        if search.isdigit():
            query = query.filter(Trek.id == int(search))
        else:
            query= query.filter(Trek.name.ilike(f"%{search}%"))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if duration:
        if duration =="1-3":
            query = query.filter(Trek.duration.between(1,3))
        elif duration == "4-6":
            query = query.filter(Trek.duration.between(4,6))
        else :
            query = query.filter(Trek.duration >= 7)
            
    treks = query.all()
    return render_template('admin/manage_trek.html',treks=treks)



@admin_bp.route('/add_trek',methods=['GET', 'POST'])
def add_trek():
    staffs = User.query.filter_by(role='staff',status='Active').all()
    if request.method == "POST":
        name = request.form.get('name')
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')
        duration  = request.form.get('duration')
        available_slots = request.form.get('available_slots')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        assign_id = request.form.get('assign_id')
        description = request.form.get('description')
        if not name and not location and not available_slots and not start_date and not end_date:
            flash("Please fill all required fields.","danger")
            return redirect(url_for('admin.add_trek'))
        
        new_trek = Trek(
            name = name,
            location = location,
            difficulty = difficulty,
            duration  = int(duration),
            available_slots = int(available_slots),
            start_date = datetime.strptime(start_date,'%Y-%m-%d').date(),
            end_date = datetime.strptime(end_date,'%Y-%m-%d').date(),
            assigned_staff_id = assign_id,
            description=description,
            status='Approved'
        )
        db.session.add(new_trek)
        flash('New trek added.','success')
        db.session.commit()
    return render_template('admin/add_trek.html',staffs=staffs)


@admin_bp.route('/treks/edits/<int:trek_id>',methods=['GET','POST'])
def edit_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    staffs = User.query.filter_by(role='staff',status='Active').all()
    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration  = request.form.get('duration')
        trek.available_slots = request.form.get('available_slots')
        trek.start_date = datetime.strptime(request.form.get('start_date'),'%Y-%m-%d').date()
        trek.end_date = datetime.strptime(request.form.get('end_date'),'%Y-%m-%d').date()
        trek.assigned_staff_id = request.form.get('assign_id')
        trek.description = request.form.get('description')
        trek.status = request.form.get('status')
        db.session.commit()
        flash('Trek Updated successfully.','success')
        return redirect(url_for('admin.manage_treks'))
    
    return render_template('admin/edit_trek.html',trek=trek,staffs=staffs)

@admin_bp.route('/treks/delete/<int:trek_id>')
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    flash('Trek deleted.','info')
    return redirect(url_for('admin.manage_treks'))


@admin_bp.route('/staff')
@login_required
@admin_required
def manage_staff(): 
    query = User.query.filter_by(role='staff')
    search = request.args.get('search')
    if search:
        if search.isdigit():
            query = query.filter(User.id == int(search))
        else:
            query= query.filter(User.name.ilike(f"%{search}%"))
            
    staffs = query.all()
    
    pending = [staff for staff in staffs if staff.status == "Pending"]
    active = [staff for staff in staffs if staff.status == "Active"]
    blacklisted = [staff for staff in staffs if staff.status == "Blacklisted"]
    
    staff_treks = {}

    for staff in active:
        staff_treks[staff.id] = Trek.query.filter_by(
        assigned_staff_id=staff.id
    ).all()
    return render_template('admin/manage_staff.html',
                           active = active,
                           pending = pending,
                           blacklisted=blacklisted,
                           staff_treks=staff_treks)


# approve staff
@admin_bp.route('/staff/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_staff(user_id):
    user = db.session.get(User,user_id)
    if not user or user.role != 'staff':
        flash("Not a Staff Account",'danger')
        redirect(url_for('admin.manage_staff'))
      
    user.status ="Active"
    
    db.session.commit()
    flash(f'{user.name} approved successfully.', 'success')
    return redirect(url_for('admin.manage_staff'))

# blacklist
@admin_bp.route('/staff/<int:user_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_staff(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'Blacklisted'
    db.session.commit()
    flash(f'{user.name} has been blacklisted.', 'warning')
    return redirect(url_for('admin.manage_staff'))

# reactivate
@admin_bp.route('/staff/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_staff(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'Pending'
    
    db.session.commit()
    flash(f'{user.name} reactivated.', 'success')
    return redirect(url_for('admin.manage_staff'))
   
    
@admin_bp.route('/user')
@login_required
@admin_required
def manage_user():
       
    query = User.query.filter_by(role='trekker')
    search = request.args.get('search')
    if search:
        if search.isdigit():
            query = query.filter(User.id == int(search))
        else:
            query= query.filter(User.name.ilike(f"%{search}%"))
            
    trekkers = query.all()
    user = [trekker for trekker in trekkers if trekker.status == "Active"]
    blacklisted = [trekker for trekker in trekkers if trekker.status == "Blacklisted"]
    
    return render_template('admin/admin_manage_user.html',user=user,blacklisted = blacklisted)



# blacklist
@admin_bp.route('/user/<int:user_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'Blacklisted'
    db.session.commit()
    flash(f'{user.name} has been blacklisted.', 'warning')
    return redirect(url_for('admin.manage_user'))

# reactivate 
@admin_bp.route('/user/<int:user_id>/reactivate',methods=['POST'])
@login_required
@admin_required
def reactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'Active'
    db.session.commit()
    flash(f'{user.name} has been reactivated.','success')
    return redirect(url_for('admin.manage_user'))

@admin_bp.route('/bookings')
@login_required
@admin_required
def manage_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    booked = Booking.query.filter_by(status='Booked').all()
    completed = Booking.query.filter_by(status ='Completed').all()
    cancelled = Booking.query.filter_by(status='Cancelled').all()
    return render_template('admin/manage_bookings.html',
                           bookings = bookings,
                           booked=booked,
                           completed=completed,
                           cancelled=cancelled)

@admin_bp.route('/profile',methods=['GET','POST'])
@login_required
@admin_required
def profile():
    admin = User.query.filter_by(role='admin').first()
    if request.method == "POST":
        name=request.form.get('name')
        phone_no=request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        blood_group = request.form.get('blood_group')
        address = request.form.get('address')
        
        admin.name = name
        admin.phone = phone_no
        admin.dob = datetime.strptime(dob,'%Y-%m-%d').date()
        admin.gender = gender
        admin.blood_group = blood_group
        admin.address = address
        
        db.session.commit()
        flash("Profile Updated",'success')
        
    return render_template('admin/admin_profile.html',admin=admin)

