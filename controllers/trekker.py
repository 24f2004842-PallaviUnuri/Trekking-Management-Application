from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User,Trek,Booking
from flask_login import login_user, logout_user, login_required, current_user  # type: ignore
from sqlalchemy import func, extract
from calendar import month_abbr
from datetime import datetime,date
trekker_bp = Blueprint('trekker',__name__)

@trekker_bp.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    total_bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    upcoming_treks = Booking.query.filter_by(
        user_id=current_user.id,
        status="Booked"
    ).count()

    completed_treks = Booking.query.filter_by(
        user_id=current_user.id,
        status="Completed"
    ).count()

    cancelled_treks = Booking.query.filter_by(
        user_id=current_user.id,
        status="Cancelled"
    ).count()
    
    

    next_booking = (
        Booking.query.filter_by(
            user_id=current_user.id,
            status="Booked"
        )
        .order_by(Booking.booking_date.desc())
        .first()
    )
    recent_bookings = (
        Booking.query.filter_by(user_id=current_user.id)
        .order_by(Booking.booking_date.desc())
        .limit(5)
        .all()
    )
    #Current year
    current_year = datetime.now().year

    #Extract month from booking_date
    booking_month = extract("month", Booking.booking_date)

    #Extract year from booking_date
    booking_year = extract("year", Booking.booking_date)

    #Query monthly bookings
    booking_data = (
        db.session.query(
            booking_month.label("month"),
            func.count(Booking.id).label("count")
        )
        .filter(
            Booking.user_id == current_user.id,
            booking_year == current_year
        )
        .group_by(booking_month)
        .all()
    )
    months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    monthly_bookings = [0] * 12

    for month, count in booking_data:
        monthly_bookings[int(month) - 1] = count
        
        
    
    return render_template('trekker/trekker_dashboard.html',
                           total_bookings=total_bookings,
        upcoming_treks=upcoming_treks,
        completed_treks=completed_treks,
        cancelled_treks=cancelled_treks,
        next_booking=next_booking,
        recent_bookings=recent_bookings,
         months=months,
        monthly_bookings=monthly_bookings)

@trekker_bp.route('/treks',methods=['GET'])
@login_required
def treks():
    query = Trek.query.filter_by(status = "Open")
    #search 
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
    
    booked_trek_id = {
        booking.trek_id
        for booking in current_user.bookings
        if booking.status == 'Booked'
    }

    return render_template('trekker/treks.html' , treks = treks,booked_trek_id=booked_trek_id)

# book trek
@trekker_bp.route('/book_trek/<int:trek_id>',methods=['POST'])
@login_required
def book_trek(trek_id):
    
    trek = Trek.query.get_or_404(trek_id)
    if trek.available_slots <= 0:
        flash(f'No slot available in {trek.name}','warning')
        return redirect(url_for('trekker.treks'))
    # checking if user has already booked 
    existing_booking = Booking.query.filter_by(
        user_id = current_user.id,
        trek_id = trek.id
    ).first()
    if existing_booking:
        
        if existing_booking.status == "Cancelled":
            existing_booking.status = "Booked"
            existing_booking.booking_date = datetime.now()
            trek.available_slots -= 1
            
        else:
            flash(f'You have already booked this { trek.name }','warning')
            return redirect(url_for('trekker.treks'))
    else:
        
    #create a new booking
        booking = Booking(
            user_id = current_user.id,
            trek_id = trek.id
        )
        db.session.add(booking)
        trek.available_slots -= 1
    
    db.session.commit()
    flash(f'Booking successful for {trek.name}','success')
    
    return redirect(url_for('trekker.treks'))





@trekker_bp.route('/bookings',methods=['GET','POST'])
@login_required
def bookings():  
    query = Booking.query.filter_by(user_id = current_user.id)
    query = query.join(Booking.trek)
    #search for booked trek page
    search = request.args.get('search')
    difficulty = request.args.get('difficulty')
    duration = request.args.get('duration')
    if search:
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
    booked_trek=query.all()
    return render_template('trekker/bookings.html',booked_trek=booked_trek)



#cancel trek booking
@trekker_bp.route('/cancel_trek/<int:trek_id>',methods=['POST'])
@login_required
def cancel_trek(trek_id):
    trek = db.session.get(Trek,trek_id)
    booking = Booking.query.filter_by(
        trek_id = trek.id ,
        user_id = current_user.id).first_or_404()
    
    booking.status="Cancelled"
    
    trek.available_slots += 1
    db.session.commit()
    flash(f"'{trek.name}' booking cancelled.", "warning")
    
    return redirect(url_for('trekker.bookings'))

@trekker_bp.route('/history',methods=['GET','POST'])
@login_required
def history():
    query = Booking.query.filter_by(user_id=current_user.id)
    query = query.join(Booking.trek)
    
    # Search
    search = request.args.get('search')
    if search:
        query = query.filter(Trek.name.ilike(f"%{search}%"))
    # Status filter
    status = request.args.get('status')
    if status:
        query = query.filter(Booking.status == status)
    else:
        query = query.filter(Booking.status.in_(["Completed", "Cancelled"]))
        
    history = query.all()
    
    # for card 
    total_history = Booking.query.filter(
    Booking.user_id == current_user.id,
    Booking.status.in_(["Completed", "Cancelled"])).count()

    completed = Booking.query.filter_by(
    user_id=current_user.id,
    status="Completed").count()

    cancelled = Booking.query.filter_by(
    user_id=current_user.id,
    status="Cancelled").count()
    return render_template('trekker/history.html',history=history,
                        total_history=total_history,
                        completed=completed,
                        cancelled=cancelled)

@trekker_bp.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    trekker = User.query.filter(User.id == current_user.id).first_or_404()
    
    if request.method == "POST":
        name=request.form.get('name')
        phone_no=request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        blood_group = request.form.get('blood_group')
        address = request.form.get('address')
        
        trekker.name = name
        trekker.phone = phone_no
        trekker.dob = datetime.strptime(dob,'%Y-%m-%d').date()
        trekker.gender = gender
        trekker.blood_group = blood_group
        trekker.address = address
        
        db.session.commit()
        flash("Profile Updated",'success')
    
    return render_template('trekker/profile.html',trekker=trekker)

