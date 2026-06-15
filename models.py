from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime , timezone
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id            = db.Column(db.Integer , primary_key=True)
    name          = db.Column(db.String(100) , nullable=False)
    password      = db.Column(db.String(255) , nullable=False)
    email         = db.Column(db.String(254),nullable=False,unique=True)
    phone         = db.Column(db.String(30))
    dob           = db.Column(db.DateTime)
    role          = db.Column(db.String(30),default="Trekker")
    status        = db.Column(db.String(30),default="Active")
    
    # relationship

    bookings = db.relationship('Booking',back_populates='user')
    staff_profile = db.relationship('StaffProfile',back_populates='user')

class Trek(db.Model):
    __tablename__ = "trek"
    
    id                = db.Column(db.Integer , primary_key = True)
    name              = db.Column(db.String(100),nullable=False)
    location          = db.Column(db.String(300),nullable=False)
    difficulty        = db.Column(db.String(35),nullable=False)
    duration          = db.Column(db.Integer,nullable=False)
    available_slots   = db.Column(db.Integer,nullable=False)
    status            = db.Column(db.String,default="Pending")                                  # (Pending / Approved / Open / Closed / Completed)
    description       = db.Column(db.Text)
    start_date        = db.Column(db.String(20),nullable=False)
    end_date          = db.Column(db.String(20),nullable=False)
    assigned_staff_id = db.Column(db.Integer,db.ForeignKey('staff_profiles.id'),nullable=True)
    
                                                                       #relationship
    bookings = db.relationship('Booking',back_populates='trek')        #one trek has many bookings
    staff    = db.relationship('StaffProfile',back_populates='treks')  #one trek is assigned to one staff
    
#Booking table
class Booking(db.Model):
    __tablename__ = "booking"
    id            = db.Column(db.Integer , primary_key = True)
    user_id       = db.Column(db.Integer,db.ForeignKey('users.id'))
    trek_id       = db.Column(db.Integer,db.ForeignKey('trek.id'))
    booking_date  = db.Column(db.DateTime , default= lambda : datetime.now(timezone.utc))
    status        = db.Column(db.String(20),default="Booked")
    
    user = db.relationship('User' , back_populates = 'bookings')
    trek = db.relationship('Trek' , back_populates = 'bookings' )



class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"
    id            = db.Column(db.Integer , primary_key=True)
    user_id       = db.Column(db.Integer , db.ForeignKey('users.id'))
    name          = db.Column(db.String(100),nullable=False)
    contact       = db.Column(db.String(100))
    status        = db.Column(db.String(20),default="Pending")
    
    #relationship
    
    user  = db.relationship('User',back_populates='staff_profile')
    treks = db.relationship('Trek',back_populates='staff')
    