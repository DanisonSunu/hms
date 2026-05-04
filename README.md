# Hospital Management System (HMS)
## Flask + Bootstrap + SQLite | BTech CSE Project

A complete, modular Hospital Management System built with Python Flask backend,
Bootstrap 5 frontend, and SQLite database.

---

## Project Structure

```
hms/
├── app.py                  # Main app factory + database seeding
├── requirements.txt        # Python dependencies
├── schema.sql              # Raw SQL schema (reference)
│
├── models/                 # SQLAlchemy ORM models
│   ├── database.py         # db instance
│   ├── user.py             # Auth user (Flask-Login)
│   ├── patient.py
│   ├── doctor.py
│   ├── staff.py
│   ├── appointment.py
│   ├── record.py           # MedicalRecord
│   ├── billing.py
│   └── inventory.py
│
├── routes/                 # Flask Blueprints (one per module)
│   ├── auth.py             # Login / Logout
│   ├── dashboard.py        # Home dashboard
│   ├── patients.py         # Patient CRUD
│   ├── doctors.py          # Doctor CRUD
│   ├── staff.py            # Staff CRUD
│   ├── appointments.py     # Appointment CRUD + status AJAX
│   ├── records.py          # Medical Records CRUD
│   ├── billing.py          # Billing CRUD + pay AJAX
│   └── inventory.py        # Inventory CRUD + restock AJAX
│
└── templates/              # Jinja2 HTML templates
    ├── base.html           # Shared layout (sidebar, navbar)
    ├── dashboard.html
    ├── auth/login.html
    ├── patients/           # list, add, edit, detail
    ├── doctors/            # list, add, edit
    ├── staff/              # list, add, edit
    ├── appointments/       # list, add, edit
    ├── records/            # list, add, edit, detail
    ├── billing/            # list, add, edit
    └── inventory/          # list, add, edit
```

---

## Setup Instructions

### 1. Create & activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

The app auto-creates the SQLite database and seeds it with sample data
on first run. Open http://localhost:5000 in your browser.

---

## Default Login Credentials

| Role   | Username | Password   | Access                                  |
|--------|----------|------------|-----------------------------------------|
| Admin  | admin    | admin123   | Full access to all modules              |
| Doctor | doctor1  | doctor123  | Appointments + Medical Records          |
| Staff  | staff1   | staff123   | Patients + Appointments + Billing       |

---

## Features & Modules

### 1. Authentication System
- Session-based login/logout using Flask-Login
- Passwords stored as bcrypt hashes
- Role-based access control (Admin / Doctor / Staff)
- Automatic redirect to login for unauthenticated access

### 2. Patient Management
- Register new patients (name, age, gender, phone, blood group, address)
- Search patients by name or phone number
- View full patient profile with tabs for appointments, records, bills
- Edit and delete patient records

### 3. Doctor Management (Admin only)
- Add/edit/remove doctors with specialization and experience
- Toggle availability status
- Filter by specialization
- Card-based grid UI

### 4. Staff Management (Admin only)
- Full CRUD for hospital staff
- Roles: Nurse, Receptionist, Lab Technician, Pharmacist, etc.
- Department assignment

### 5. Appointment Scheduling
- Book appointments linking a patient to a doctor
- Date + time slot selection with conflict detection
- Status tracking: Scheduled / Completed / Cancelled
- Doctors see only their own appointments
- AJAX quick status update endpoint

### 6. Medical Records
- Create detailed records: diagnosis, prescription, notes
- Linked to patient and attending doctor
- Doctors see only records they created
- Staff have no access (privacy)

### 7. Billing System
- Create bills with amount and description
- Payment status: Pending / Paid / Cancelled
- One-click AJAX "Mark as Paid" button
- Revenue summary cards (Total Billed, Collected, Pending)

### 8. Inventory Management (Admin + Staff)
- Track medicines, equipment, and consumables
- Low stock alert (< 50 units highlighted in red)
- AJAX restock modal — add quantity without page reload
- Category filter

### 9. Dashboard
- Real-time statistics cards (patients, doctors, revenue, etc.)
- Recent appointments table
- Role-specific quick action buttons

---

## API Endpoints Summary

### Auth
| Method | URL               | Description        |
|--------|-------------------|--------------------|
| GET    | /auth/login       | Show login page    |
| POST   | /auth/login       | Process login      |
| GET    | /auth/logout      | Log out            |

### Patients
| Method | URL                       | Description           |
|--------|---------------------------|-----------------------|
| GET    | /patients/                | List all patients     |
| GET    | /patients/add             | Add form              |
| POST   | /patients/add             | Create patient        |
| GET    | /patients/<id>            | View patient          |
| GET    | /patients/edit/<id>       | Edit form             |
| POST   | /patients/edit/<id>       | Update patient        |
| POST   | /patients/delete/<id>     | Delete patient        |
| GET    | /patients/api/all         | JSON list             |

### Appointments
| Method | URL                           | Description           |
|--------|-------------------------------|-----------------------|
| GET    | /appointments/                | List appointments     |
| POST   | /appointments/add             | Book appointment      |
| POST   | /appointments/edit/<id>       | Update appointment    |
| POST   | /appointments/delete/<id>     | Delete appointment    |
| POST   | /appointments/status/<id>     | AJAX status update    |

### Billing
| Method | URL                   | Description       |
|--------|-----------------------|-------------------|
| GET    | /billing/             | List bills        |
| POST   | /billing/add          | Create bill       |
| POST   | /billing/edit/<id>    | Update bill       |
| POST   | /billing/delete/<id>  | Delete bill       |
| POST   | /billing/pay/<id>     | AJAX mark paid    |

### Inventory
| Method | URL                       | Description       |
|--------|---------------------------|-------------------|
| GET    | /inventory/               | List items        |
| POST   | /inventory/add            | Add item          |
| POST   | /inventory/edit/<id>      | Update item       |
| POST   | /inventory/delete/<id>    | Remove item       |
| POST   | /inventory/restock/<id>   | AJAX restock      |

---

## Database Schema

```sql
Users(user_id, username, password, role, linked_id, created_at)
Patients(patient_id, name, age, gender, phone, address, blood_group, registration_date)
Doctors(doctor_id, name, specialization, phone, email, experience, available)
Staff(staff_id, name, role, phone, email, department, join_date)
Appointments(appointment_id, patient_id*, doctor_id*, date, time, status, notes, created_at)
Medical_Records(record_id, patient_id*, doctor_id*, diagnosis, prescription, notes, date)
Billing(bill_id, patient_id*, amount, description, payment_status, billing_date)
Inventory(item_id, item_name, category, quantity, unit, supplier, unit_price, last_updated)
```
*Foreign key

---

## Technologies Used

| Layer     | Technology                  |
|-----------|-----------------------------|
| Backend   | Python 3, Flask 3.0         |
| ORM       | Flask-SQLAlchemy 3.1        |
| Auth      | Flask-Login 0.6             |
| Database  | SQLite (via SQLAlchemy)     |
| Frontend  | Bootstrap 5.3, Bootstrap Icons |
| Fonts     | Google Fonts (Outfit, Inter)|
| JS        | Vanilla JS + Fetch API      |
