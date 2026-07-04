from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User,StaffProfile
from flask_login import login_user, logout_user, login_required 
from werkzeug.security import generate_password_hash, check_password_hash 

trekker_bp = Blueprint('trekker',__name__)

@trekker_bp.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('trekker/trekker_dashboard.html')