from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User,Trek,Booking
from flask_login import login_user, logout_user, login_required, current_user  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
trekker_bp = Blueprint('trekker',__name__)

@trekker_bp.route('/dashboard',methods=['GET','POST'])
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
    return render_template('trekker/trekker_dashboard.html',
                           total_bookings=total_bookings,
        upcoming_treks=upcoming_treks,
        completed_treks=completed_treks,
        cancelled_treks=cancelled_treks,
        next_booking=next_booking,
        recent_bookings=recent_bookings)

@trekker_bp.route('/treks',methods=['GET'])
def treks():
    query = Trek.query.filter_by(status = "Open")
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
    treks = query.all()
    return render_template('trekker/treks.html' , treks = treks)

# book trek
@trekker_bp.route('/book_trek/<int:trek_id>',methods=['POST'])
def book_trek(trek_id):
    
    trek = Trek.query.get_or_404(trek_id)
    if trek.available_slots <= 0:
        flash(f'No slot available in {trek.name}','warning')
        return redirect(url_for('trekker.treks'))
    # checking if user has already booked 
    existing_booking = Booking.query.filter_by(
        user_id = current_user.id,
        trek_id = trek.id,
        status = 'Booked'
    ).first()
    if existing_booking:
        flash(f'You have already booked this { trek.name }','warning')
        return redirect(url_for('trekker.treks'))
    
    #create a booking
    booking = Booking(
        user_id = current_user.id,
        trek_id = trek.id
    )
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    flash(f'Booking successful for {trek.name}','success')
    
    return redirect(url_for('trekker.treks'))





@trekker_bp.route('/bookings',methods=['GET','POST'])
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
def profile():
    trekker = User.query.filter_by(id = current_user.id).first_or_404()
    
    if request.method == "POST":
        name = request.form.get("name")
        phone_no = request.form.get("contact")
        dob = request.form.get('dob')
        
        trekker.name = name
        trekker.phone = phone_no
        trekker.dob = datetime.strptime(dob,'%Y-%m-%d').date()
        
        db.session.commit()
        flash("Details changed",'success')
    
    return render_template('trekker/profile.html',trekker=trekker)

