import os
import random
from datetime import datetime, timedelta
from app import app, db
from models import User, Trek, Booking

# Define trek data without hardcoded assigned_staff_id
TREK_DATA = [
    {
        "name": "Rajmachi Fort",
        "location": "Maharashtra",
        "difficulty": "Easy",
        "duration": 2,
        "total_slots": 25,
        "status": "Open",
        "description": "A beautiful easy trek through Rajmachi Fort in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-02-02",
        "end_date": "2026-02-04",
    },
    {
        "name": "Harishchandragad",
        "location": "Maharashtra",
        "difficulty": "Moderate",
        "duration": 3,
        "total_slots": 30,
        "status": "Open",
        "description": "A beautiful moderate trek through Harishchandragad in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-03-03",
        "end_date": "2026-03-06",
    },
    {
        "name": "Kalsubai Peak",
        "location": "Maharashtra",
        "difficulty": "Hard",
        "duration": 4,
        "total_slots": 35,
        "status": "Open",
        "description": "A beautiful hard trek through Kalsubai Peak in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-04-04",
        "end_date": "2026-04-08",
    },
    {
        "name": "Triund",
        "location": "Himachal Pradesh",
        "difficulty": "Easy",
        "duration": 5,
        "total_slots": 40,
        "status": "Approved",
        "description": "A beautiful easy trek through Triund in Himachal Pradesh, suitable for adventure enthusiasts.",
        "start_date": "2026-05-05",
        "end_date": "2026-05-10",
    },
    {
        "name": "Kedarkantha",
        "location": "Uttarakhand",
        "difficulty": "Moderate",
        "duration": 1,
        "total_slots": 45,
        "status": "Closed",
        "description": "A beautiful moderate trek through Kedarkantha in Uttarakhand, suitable for adventure enthusiasts.",
        "start_date": "2026-06-06",
        "end_date": "2026-06-07",
    },
    {
        "name": "Valley of Flowers",
        "location": "Uttarakhand",
        "difficulty": "Hard",
        "duration": 2,
        "total_slots": 20,
        "status": "Completed",
        "description": "A beautiful hard trek through Valley of Flowers in Uttarakhand, suitable for adventure enthusiasts.",
        "start_date": "2026-07-07",
        "end_date": "2026-07-09",
    },
    {
        "name": "Hampta Pass",
        "location": "Himachal Pradesh",
        "difficulty": "Easy",
        "duration": 3,
        "total_slots": 25,
        "status": "Open",
        "description": "A beautiful easy trek through Hampta Pass in Himachal Pradesh, suitable for adventure enthusiasts.",
        "start_date": "2026-08-08",
        "end_date": "2026-08-11",
    },
    {
        "name": "Tadiandamol",
        "location": "Karnataka",
        "difficulty": "Moderate",
        "duration": 4,
        "total_slots": 30,
        "status": "Open",
        "description": "A beautiful moderate trek through Tadiandamol in Karnataka, suitable for adventure enthusiasts.",
        "start_date": "2026-09-09",
        "end_date": "2026-09-13",
    },
    {
        "name": "Kumara Parvatha",
        "location": "Karnataka",
        "difficulty": "Hard",
        "duration": 5,
        "total_slots": 35,
        "status": "Open",
        "description": "A beautiful hard trek through Kumara Parvatha in Karnataka, suitable for adventure enthusiasts.",
        "start_date": "2026-10-10",
        "end_date": "2026-10-15",
    },
    {
        "name": "Chembra Peak",
        "location": "Kerala",
        "difficulty": "Easy",
        "duration": 1,
        "total_slots": 40,
        "status": "Approved",
        "description": "A beautiful easy trek through Chembra Peak in Kerala, suitable for adventure enthusiasts.",
        "start_date": "2026-11-11",
        "end_date": "2026-11-12",
    },
    {
        "name": "Agasthyakoodam",
        "location": "Kerala",
        "difficulty": "Moderate",
        "duration": 2,
        "total_slots": 45,
        "status": "Closed",
        "description": "A beautiful moderate trek through Agasthyakoodam in Kerala, suitable for adventure enthusiasts.",
        "start_date": "2026-12-12",
        "end_date": "2026-12-14",
    },
    {
        "name": "Sandakphu",
        "location": "West Bengal",
        "difficulty": "Hard",
        "duration": 3,
        "total_slots": 20,
        "status": "Completed",
        "description": "A beautiful hard trek through Sandakphu in West Bengal, suitable for adventure enthusiasts.",
        "start_date": "2026-01-13",
        "end_date": "2026-01-16",
    },
    {
        "name": "Dzukou Valley",
        "location": "Nagaland",
        "difficulty": "Easy",
        "duration": 4,
        "total_slots": 25,
        "status": "Open",
        "description": "A beautiful easy trek through Dzukou Valley in Nagaland, suitable for adventure enthusiasts.",
        "start_date": "2026-02-14",
        "end_date": "2026-02-18",
    },
    {
        "name": "Goechala",
        "location": "Sikkim",
        "difficulty": "Moderate",
        "duration": 5,
        "total_slots": 30,
        "status": "Open",
        "description": "A beautiful moderate trek through Goechala in Sikkim, suitable for adventure enthusiasts.",
        "start_date": "2026-03-15",
        "end_date": "2026-03-20",
    },
    {
        "name": "Brahmatal",
        "location": "Uttarakhand",
        "difficulty": "Hard",
        "duration": 1,
        "total_slots": 35,
        "status": "Open",
        "description": "A beautiful hard trek through Brahmatal in Uttarakhand, suitable for adventure enthusiasts.",
        "start_date": "2026-04-16",
        "end_date": "2026-04-17",
    },
    {
        "name": "Nag Tibba",
        "location": "Uttarakhand",
        "difficulty": "Easy",
        "duration": 2,
        "total_slots": 40,
        "status": "Approved",
        "description": "A beautiful easy trek through Nag Tibba in Uttarakhand, suitable for adventure enthusiasts.",
        "start_date": "2026-05-17",
        "end_date": "2026-05-19",
    },
    {
        "name": "Dayara Bugyal",
        "location": "Uttarakhand",
        "difficulty": "Moderate",
        "duration": 3,
        "total_slots": 45,
        "status": "Closed",
        "description": "A beautiful moderate trek through Dayara Bugyal in Uttarakhand, suitable for adventure enthusiasts.",
        "start_date": "2026-06-18",
        "end_date": "2026-06-21",
    },
    {
        "name": "Sinhagad Night Trek",
        "location": "Maharashtra",
        "difficulty": "Hard",
        "duration": 4,
        "total_slots": 20,
        "status": "Completed",
        "description": "A beautiful hard trek through Sinhagad Night Trek in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-07-19",
        "end_date": "2026-07-23",
    },
    {
        "name": "Torna Fort",
        "location": "Maharashtra",
        "difficulty": "Easy",
        "duration": 5,
        "total_slots": 25,
        "status": "Open",
        "description": "A beautiful easy trek through Torna Fort in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-08-20",
        "end_date": "2026-08-25",
    },
    {
        "name": "Lohagad Fort",
        "location": "Maharashtra",
        "difficulty": "Moderate",
        "duration": 1,
        "total_slots": 30,
        "status": "Open",
        "description": "A beautiful moderate trek through Lohagad Fort in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-09-01",
        "end_date": "2026-09-02",
    },
    {
        "name": "Prabalgad",
        "location": "Maharashtra",
        "difficulty": "Hard",
        "duration": 2,
        "total_slots": 35,
        "status": "Open",
        "description": "A beautiful hard trek through Prabalgad in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-10-02",
        "end_date": "2026-10-04",
    },
    {
        "name": "Korigad",
        "location": "Maharashtra",
        "difficulty": "Easy",
        "duration": 3,
        "total_slots": 40,
        "status": "Approved",
        "description": "A beautiful easy trek through Korigad in Maharashtra, suitable for adventure enthusiasts.",
        "start_date": "2026-11-03",
        "end_date": "2026-11-06",
    },
    {
        "name": "Mullayanagiri",
        "location": "Karnataka",
        "difficulty": "Moderate",
        "duration": 4,
        "total_slots": 45,
        "status": "Closed",
        "description": "A beautiful moderate trek through Mullayanagiri in Karnataka, suitable for adventure enthusiasts.",
        "start_date": "2026-12-04",
        "end_date": "2026-12-08",
    },
    {
        "name": "Netravati Peak",
        "location": "Karnataka",
        "difficulty": "Hard",
        "duration": 5,
        "total_slots": 20,
        "status": "Completed",
        "description": "A beautiful hard trek through Netravati Peak in Karnataka, suitable for adventure enthusiasts.",
        "start_date": "2026-01-05",
        "end_date": "2026-01-10",
    },
    {
        "name": "Kudremukh",
        "location": "Karnataka",
        "difficulty": "Easy",
        "duration": 1,
        "total_slots": 25,
        "status": "Open",
        "description": "A beautiful easy trek through Kudremukh in Karnataka, suitable for adventure enthusiasts.",
        "start_date": "2026-02-06",
        "end_date": "2026-02-07",
    }
]

import os
import random
from datetime import datetime, timedelta
from app import app, db
from models import User, Trek, Booking
from werkzeug.security import generate_password_hash

def seed_all():
    print("Initializing Database Seeding...")
    with app.app_context():
        # Step 1: Clean existing data (avoiding migration table drop)
        print("Clearing existing data...")
        Booking.query.delete()
        Trek.query.delete()
        User.query.delete()
        db.session.commit()

        # Step 2: Seed Admin
        print("Seeding Admin User...")
        admin = User(
            name="admin",
            email="admin@admin.com",
            password=generate_password_hash("pass"),
            role="admin",
            status="Active"
        )
        db.session.add(admin)

        # Step 3: Seed Trekkers (20 users)
        print("Seeding Trekkers...")
        trekkers = []
        for i in range(1, 21):
            trekker = User(
                name=f"Trekker {i}",
                password=generate_password_hash("pass123"),
                email=f"trekker{i}@example.com",
                phone=f"900000{1000+i}",
                dob=datetime.strptime(f"199{i%10}-0{(i%9)+1}-15", "%Y-%m-%d").date(),
                gender="Male" if i % 2 else "Female",
                blood_group=["A+", "B+", "O+", "AB+"][i % 4],
                address=f"Address {i}",
                role="trekker",
                status="Blacklisted" if i in (5, 10, 15, 20) else "Active"
            )
            db.session.add(trekker)
            trekkers.append(trekker)
        db.session.commit() # Commit to generate IDs

        # Step 4: Seed Staff (20 users)
        print("Seeding Staff members...")
        staff_list = []
        for i in range(1, 21):
            if i <= 8:
                status = "Pending"
            elif i <= 16:
                status = "Active"
            else:
                status = "Blacklisted"
            
            staff = User(
                name=f"Staff {i}",
                password=generate_password_hash("pass123"),
                email=f"staff{i}@example.com",
                phone=f"800000{1000+i}",
                dob=datetime.strptime(f"198{i%10}-0{(i%9)+1}-20", "%Y-%m-%d").date(),
                gender="Male" if i % 2 else "Female",
                blood_group=["A+", "B+", "O+", "AB+"][i % 4],
                address=f"Staff Address {i}",
                role="staff",
                status=status
            )
            db.session.add(staff)
            staff_list.append(staff)
        db.session.commit() # Commit to generate IDs

        # Fetch active staff members to assign treks
        active_staff = User.query.filter_by(role="staff", status="Active").all()
        if not active_staff:
            print("ERROR: No active staff found. Make sure some staff have status='Active'.")
            return

        # Step 5: Seed Treks (assign dynamically)
        print("Seeding Treks...")
        seeded_treks = []
        today = datetime.now().date()
        for idx, t in enumerate(TREK_DATA):
            # Pick an active staff member round-robin style
            staff_assigned = active_staff[idx % len(active_staff)]
            
            start_date = datetime.strptime(t["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(t["end_date"], "%Y-%m-%d").date()
            
            if end_date < today:
                status = "Completed"
            elif start_date <= today <= end_date:
                status = "Closed"
            else:
                status = "Open"
            
            trek = Trek(
                name=t["name"],
                location=t["location"],
                difficulty=t["difficulty"],
                duration=t["duration"],
                total_slots=t["total_slots"],
                available_slots=t["total_slots"],  # Will adjust based on booking count
                status=status,
                description=t["description"],
                start_date=start_date,
                end_date=end_date,
                assigned_staff_id=staff_assigned.id
            )
            db.session.add(trek)
            seeded_treks.append(trek)
        db.session.commit()

        # Step 6: Seed Bookings
        print("Seeding Bookings...")
        # Get active trekkers
        active_trekkers = User.query.filter_by(role="trekker", status="Active").all()
        booking_count = 0
        
        for trek in seeded_treks:
            # Determine booking count for this trek: between 4 and min(12, trekkers count)
            num_bookings = random.randint(4, min(len(active_trekkers), 12))
            eligible_trekkers = random.sample(active_trekkers, num_bookings)

            booked_slots = 0
            for trekker in eligible_trekkers:
                if trek.status in ["Completed", "Closed"]:
                    booking_status = "Completed"
                else:
                    booking_status = "Booked"
                
                # Make booking_date before the start date
                booking_date = trek.start_date - timedelta(days=random.randint(5, 30))
                booking_datetime = datetime.combine(booking_date, datetime.min.time())
                
                booking = Booking(
                    user_id=trekker.id,
                    trek_id=trek.id,
                    booking_date=booking_datetime,
                    status=booking_status
                )
                db.session.add(booking)
                booking_count += 1
                
                # Decrement available slots only if booking is active
                if booking_status == "Booked":
                    booked_slots += 1
            
            trek.available_slots = max(0, trek.total_slots - booked_slots)

        db.session.commit()
        print(f"Successfully seeded {len(active_trekkers)} Trekkers, {len(staff_list)} Staff, {len(seeded_treks)} Treks, and {booking_count} Bookings.")

if __name__ == "__main__":
    seed_all()
