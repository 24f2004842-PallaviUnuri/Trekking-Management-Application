from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin

db = SQLAlchemy()

# Users Table
class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(35), nullable=False)
    password_hash = db.Column(db.String(220), nullable=False)
    role = db.Column(db.String(20), nullable=False)   # admin, staff, trekker
    status = db.Column(db.String(20), default="active")
    
    # Relationships
    bookings = db.relationship("Booking", back_populates="user")
    staff_profile = db.relationship("StaffProfile", back_populates="user", uselist=False)


# Treks Table
class Trek(db.Model):
    __tablename__ = "treks"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    slots_available = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="pending")
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    staff_id = db.Column(db.Integer, db.ForeignKey("staff_profiles.id"))
    
    # Relationships
    bookings = db.relationship("Booking", back_populates="trek")
    staff = db.relationship("StaffProfile", back_populates="treks")


# Bookings Table
class Booking(db.Model):
    __tablename__ = "bookings"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"))
    booked_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default="booked")
    
    # Relationships
    user = db.relationship("User", back_populates="bookings")
    trek = db.relationship("Trek", back_populates="bookings")


# Staff Profiles Table
class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    full_name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100))
    status = db.Column(db.String(20), default="active")
    
    # Relationships
    user = db.relationship("User", back_populates="staff_profile")
    treks = db.relationship("Trek", back_populates="staff")
