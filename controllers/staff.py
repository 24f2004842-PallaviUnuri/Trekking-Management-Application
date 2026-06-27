from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User, Trek, Booking, StaffProfile
from flask_login import login_required, current_user

staff_bp = Blueprint('staff',__name__)

@staff_bp.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('staff/staff_dashboard.html')