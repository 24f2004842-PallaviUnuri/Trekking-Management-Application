Trekking Management Application

A web-based Trekking Management Application developed using Flask that simplifies the process of managing trekking events, bookings, and participants. The system provides separate dashboards and functionalities for Admin, Trek Staff, and Trekkers through Role-Based Access Control (RBAC).

---

## 📌 Project Overview

The Trekking Management Application allows users to explore available treks, book trekking slots, monitor booking history, and track completed treks. Administrators can manage treks, users, and staff assignments, while Trek Staff handle trek operations and participant management.

The application follows the MVC architecture using Flask Blueprints and SQLAlchemy ORM.
---

## 📂 Project Structure

```
Trekking-Management/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
│
├── controllers/
│   ├── auth.py
│   ├── admin.py
│   ├── trekker.py
│   └── staff.py
│
├── templates/
│   ├── admin/
│   ├── trekker/
│   ├── staff/
│   ├── login.html
|   ├── Register.html
│   └── base.html
│
├── static/
│   ├── js/
│
└── trek.db
```

---

## 🗄️ Database Schema

### **User**

Stores information about all users, including **Admin**, **Trek Staff**, and **Trekkers**.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary Key |
| `name` | String(100) | User's full name |
| `email` | String(254) | Unique email address |
| `password` | String(255) | Hashed password |
| `phone` | String(30) | Contact number |
| `dob` | Date | Date of birth |
| `gender` | String(30) | Gender |
| `blood_group` | String(30) | Blood group |
| `address` | String(300) | Residential address |
| `role` | String(30) | User role (Admin, Trek Staff, Trekker) |
| `status` | String(30) | Account status (Active, Blacklisted, Pending) |

**Relationships**
- One user can have multiple bookings.
- Trek Staff can be assigned to multiple treks.

---

### **Trek**

Stores details of all trekking events.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary Key |
| `name` | String(100) | Trek name |
| `location` | String(300) | Trek location |
| `difficulty` | String(35) | Difficulty level |
| `duration` | Integer | Duration (in days) |
| `total_slots` | Integer | Maximum participant capacity |
| `available_slots` | Integer | Remaining available slots |
| `status` | String | Trek status (Pending, Approved, Open, Closed, Completed) |
| `description` | Text | Trek description |
| `start_date` | Date | Trek start date |
| `end_date` | Date | Trek end date |
| `assigned_staff_id` | Integer | Foreign Key referencing assigned Trek Staff |

**Relationships**
- One trek can have multiple bookings.
- Each trek can be assigned to one Trek Staff member.

---

### **Booking**

Stores booking information for trekkers.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary Key |
| `user_id` | Integer | Foreign Key → User |
| `trek_id` | Integer | Foreign Key → Trek |
| `booking_date` | DateTime | Date and time of booking |
| `status` | String(20) | Booking status (Booked, Cancelled, Completed) |

**Constraints**
- A user can book the same trek only once using a unique constraint on (`user_id`, `trek_id`).

**Relationships**
- Each booking belongs to one user.
- Each booking belongs to one trek.

---


## 🔐 User Roles

| Role | Permissions |
|------|-------------|
| Admin | Full system access |
| Trek Staff | Manage assigned treks and participants |
| Trekker | Book and manage personal treks |

---


## 📷 Screenshots

Add screenshots of:
- Register and Login Page
<img width="1915" height="790" alt="image" src="https://github.com/user-attachments/assets/50f5a8e2-b7d6-4b77-98a5-92e4458d4c19" />
<img width="1827" height="771" alt="image" src="https://github.com/user-attachments/assets/f0d60e60-cd37-417e-88c2-6c673f805999" />
- Admin Dashboard
<img width="1786" height="775" alt="image" src="https://github.com/user-attachments/assets/7a881b68-9a3c-48c5-a1de-2759c71a0b25" />
- Graphs
<img width="1817" height="785" alt="image" src="https://github.com/user-attachments/assets/7657a446-253e-470c-901b-8f269393609b" />
<img width="1802" height="808" alt="image" src="https://github.com/user-attachments/assets/f80097e7-3637-4851-9b2d-43ba2ef03cd3" />
- Booking in Trekker
<img width="1777" height="788" alt="image" src="https://github.com/user-attachments/assets/d075de06-f97a-42da-89f1-19db33ce7646" />
- Trekker Dashboard
<img width="1812" height="794" alt="image" src="https://github.com/user-attachments/assets/2aa44676-e0da-4b1a-b621-7ea3f32300c1" />
<img width="1789" height="779" alt="image" src="https://github.com/user-attachments/assets/b5a4946f-cdc1-4d4b-8153-51b1af2d67c3" />
<img width="1818" height="697" alt="image" src="https://github.com/user-attachments/assets/573e5349-9c97-4c2b-b487-10648c1f1c68" />
<img width="1809" height="785" alt="image" src="https://github.com/user-attachments/assets/f307dc3f-90d9-4488-a26e-e1d3105f693e" />
- Staff Dashboard
<img width="1825" height="774" alt="image" src="https://github.com/user-attachments/assets/b051ae46-47c9-4b3a-b265-d11f908130b2" />
<img width="1835" height="792" alt="image" src="https://github.com/user-attachments/assets/4fe30f6c-c770-4e6c-b13e-982b7035adc7" />
<img width="1830" height="793" alt="image" src="https://github.com/user-attachments/assets/199cdaf8-f33e-482c-93ff-fef4f5e756f0" />



- Profile Page
<img width="1825" height="783" alt="image" src="https://github.com/user-attachments/assets/c4e53e73-f1e3-49d1-ab82-ff293abaf6d9" />


---

## 👩‍💻 Author

**Pallavi Unuri**

BS in Data Science and Applications

IIT Madras

---

## 📄 License

This project is developed for educational purposes as part of the Modern Application Development course.
