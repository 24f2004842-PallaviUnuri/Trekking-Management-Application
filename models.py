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
    dob           = db.Column(db.Date)
    gender        = db.Column(db.String(30)) 
    blood_group   = db.Column(db.String(30))
    address       = db.Column(db.String(300))
    
    role          = db.Column(db.String(30),default="Trekker")
    status        = db.Column(db.String(30),default="Active") # Active / Blacklisted / Pending
    
    # relationship

    bookings = db.relationship('Booking',back_populates='user', cascade='all, delete-orphan')
    

class Trek(db.Model):
    __tablename__ = "trek"
    
    id                = db.Column(db.Integer , primary_key = True)
    name              = db.Column(db.String(100),nullable=False)
    location          = db.Column(db.String(300),nullable=False)
    difficulty        = db.Column(db.String(35),nullable=False)
    duration          = db.Column(db.Integer,nullable=False)
    available_slots   = db.Column(db.Integer,nullable=False)
    status            = db.Column(db.String,default="Pending")# (Pending / Approved / Open / Closed / Completed)
    description       = db.Column(db.Text)
    start_date        = db.Column(db.Date,nullable=False)
    end_date          = db.Column(db.Date,nullable=False)
    assigned_staff_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    
    #relationship
    bookings = db.relationship('Booking',back_populates='trek')        #one trek has many bookings
    staff = db.relationship('User',foreign_keys=[assigned_staff_id],backref='assigned_treks')
    
    
#Booking table
class Booking(db.Model):
    __tablename__ = "booking"
    id            = db.Column(db.Integer , primary_key = True)
    user_id       = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    trek_id       = db.Column(db.Integer,db.ForeignKey('trek.id'),nullable=False)
    booking_date  = db.Column(db.DateTime , default= lambda : datetime.now(timezone.utc))
    status        = db.Column(db.String(20),default="Booked") #Booked / Cancelled / Completed
    
    user = db.relationship('User' , back_populates = 'bookings')
    trek = db.relationship('Trek' , back_populates = 'bookings' )

    # Prevent duplicate Bookings
    __table_args__ = (db.UniqueConstraint('user_id','trek_id',name='unique_booking'),)


