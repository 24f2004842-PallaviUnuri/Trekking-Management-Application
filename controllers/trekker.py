from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User,StaffProfile,Trek,Booking
from flask_login import login_user, logout_user, login_required ,current_user
from werkzeug.security import generate_password_hash, check_password_hash 

trekker_bp = Blueprint('trekker',__name__)

@trekker_bp.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('trekker/trekker_dashboard.html')

@trekker_bp.route('/treks',methods=['GET','POST'])
def treks():
    treks = Trek.query.filter_by(status = "Open").all()
    search = request.args.get('search')
    if search : 
        treks = Trek.query.filter(Trek.name.contains(search))
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
    booked_trek = Booking.query.filter_by(user_id = current_user.id).all()
    return render_template('trekker/bookings.html',booked_trek=booked_trek)

@trekker_bp.route('/history',methods=['GET','POST'])
def history():
    return render_template('trekker/history.html')

@trekker_bp.route('/profile',methods=['GET','POST'])
def profile():
    return render_template('trekker/profile.html')

