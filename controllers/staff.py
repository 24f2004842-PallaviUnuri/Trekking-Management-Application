from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User, Trek, Booking, StaffProfile
from flask_login import login_required, current_user

staff_bp = Blueprint('staff',__name__)

@staff_bp.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    my_treks = Trek.query.filter_by(assigned_staff_id = current_user.id).all()
    total_assigned = len(my_treks)
    total_open = len([t for t in my_treks if t.status == "Open"])
    # total_participants = len()
    return render_template('staff/staff_dashboard.html',my_treks = my_treks,total_assigned=total_assigned,
                           total_open=total_open)
    

@staff_bp.route('/my_trek')
def my_trek():
    my_trek = Trek.query.filter_by(assigned_staff_id = current_user.id).all()
    return render_template('staff/my_trek.html', my_trek = my_trek)