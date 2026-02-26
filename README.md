# College Attendance Management System

A complete Django web application for managing and tracking student attendance with real-time analytics and reporting.

## Features

### 1. **Authentication System**
- Separate registration and login for Students and Faculty
- Students login using Hall Ticket ID and password
- Faculty login using username and password
- Secure Django authentication system

### 2. **Student Portal**
- View total classes, attended, and absent statistics
- Real-time attendance percentage calculation
- View predicted attendance if one more class is missed
- Red warning alert when attendance < 75%
- View detailed attendance records with dates and subjects
- Responsive dashboard with modern UI

### 3. **Faculty Portal**
- Create and manage class schedules
- View students filtered by branch and year
- Mark attendance (Present/Absent) for multiple students
- View attendance summary for all students
- Attendance statistics and analytics

### 4. **Database Design**
- Student Model: hall_ticket_id, name, branch, year, password
- Faculty Model: name, subject, branch, year (linked to Django User model)
- Schedule Model: faculty, date, subject, topic
- Attendance Model: student, schedule, status (Present/Absent)

### 5. **Key Calculations**
- Attendance % = (attended classes / total classes) × 100
- All percentages calculated dynamically (not stored in database)
- Predictive view: Shows attendance if one more class is missed

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Create a Virtual Environment
```bash
python -m venv venv
```

Activate the virtual environment:
- **On Windows:** `venv\Scripts\activate`
- **On macOS/Linux:** `source venv/bin/activate`

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create a Superuser (for Admin Panel)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 5: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### For Students

1. **Register as Student:**
   - Go to Home Page → Student Portal → Register
   - Enter Hall Ticket ID, Full Name, Branch, Year, and Password
   - Click Register

2. **Login as Student:**
   - Go to Home Page → Student Portal → Login
   - Enter Hall Ticket ID and Password
   - Access your dashboard

3. **View Attendance:**
   - Dashboard shows: Total classes, attended, absent, and percentage
   - Click "View Detailed Attendance" to see all attendance records
   - Check the predictive percentage if you miss one more class

### For Faculty

1. **Register as Faculty:**
   - Go to Home Page → Faculty Portal → Register
   - Enter Username, Full Name, Subject, Branch, Year, and Password
   - Click Register

2. **Login as Faculty:**
   - Go to Home Page → Faculty Portal → Login
   - Enter Username and Password
   - Access your dashboard

3. **Create Class Schedule:**
   - Click "Create Schedule"
   - Enter Date, Subject, and Topic
   - Click "Create Schedule"

4. **Mark Attendance:**
   - Go to "Schedules" or Dashboard
   - Click "Mark Attendance" on a schedule
   - Select Present or Absent for each student
   - Click "Save Attendance"

5. **View Student List:**
   - Click "Students" to see all students in your batch
   - View attendance statistics for each student
   - Monitor attendance trends

## Project Structure

```
edunetfinal/
├── manage.py                           # Django management script
├── requirements.txt                    # Project dependencies
├── db.sqlite3                          # SQLite database
├── attendance/                         # Main Django app
│   ├── models.py                       # Database models
│   ├── views.py                        # View logic
│   ├── forms.py                        # Form definitions
│   ├── urls.py                         # URL routing
│   ├── admin.py                        # Admin configuration
│   ├── apps.py                         # App configuration
│   └── __init__.py
├── attendanceproject/                  # Django project settings
│   ├── settings.py                     # Project settings
│   ├── urls.py                         # Main URL routing
│   ├── wsgi.py                         # WSGI configuration
│   └── __init__.py
└── templates/                          # HTML templates
    ├── base.html                       # Base template
    ├── home.html                       # Home page
    ├── register_student.html           # Student registration
    ├── login_student.html              # Student login
    ├── register_faculty.html           # Faculty registration
    ├── login_faculty.html              # Faculty login
    ├── student_dashboard.html          # Student dashboard
    ├── student_attendance_details.html # Student attendance details
    ├── faculty_dashboard.html          # Faculty dashboard
    ├── create_schedule.html            # Create schedule
    ├── mark_attendance.html            # Mark attendance
    ├── view_all_schedules.html         # View all schedules
    └── view_student_list.html          # View student list
```

## Database Models Detail

### Student Model
```python
- user (OneToOneField to Django User)
- hall_ticket_id (Unique CharField)
- name
- branch (choices: CSE, ECE, IT, ME, CE)
- year (choices: 1st, 2nd, 3rd, 4th)
```

### Faculty Model
```python
- user (OneToOneField to Django User)
- name
- subject
- branch (choices: CSE, ECE, IT, ME, CE)
- year (choices: 1st, 2nd, 3rd, 4th)
```

### Schedule Model
```python
- faculty (ForeignKey to Faculty)
- date
- subject
- topic
```

### Attendance Model
```python
- student (ForeignKey to Student)
- schedule (ForeignKey to Schedule)
- status (choices: Present, Absent)
- marked_at (DateTime)
- updated_at (DateTime)
```

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

From the admin panel, you can:
- Manage Students and Faculty profiles
- View and modify attendance records
- Create schedules manually
- Perform administrative tasks

## Calculations & Business Logic

### Attendance Percentage
- Calculated as: `(Attended Classes / Total Classes) × 100`
- Updated in real-time from the Attendance table
- Not stored in database (dynamic calculation)

### Threshold Warning
- Students get a red warning if attendance < 75%
- Shows predictions for maintaining threshold

### Predictive Attendance
- Shows what happens if student misses one more class
- Helps students plan their attendance
- Formula: `Attended / (Total + 1) × 100`

## Features Highlights

✅ **Secure Authentication** - Separate login for students and faculty
✅ **Real-time Calculations** - Attendance percentages calculated dynamically
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Bootstrap UI** - Clean and modern interface
✅ **Admin Panel** - Full Django admin integration
✅ **Data Validation** - Form validation on client and server side
✅ **Database Optimization** - Indexed fields for fast queries
✅ **Error Handling** - Proper error messages and validation

## Common Tasks

### Create a Test Student
1. Go to Register → Student
2. Hall Ticket ID: `CSE001`
3. Name: `John Doe`
4. Branch: `CSE`
5. Year: `3rd Year`
6. Password: `Test@1234`

### Create a Test Faculty
1. Go to Register → Faculty
2. Username: `prof_smith`
3. Name: `Prof. Smith`
4. Subject: `Data Structures`
5. Branch: `CSE`
6. Year: `3rd Year`
7. Password: `Prof@1234`

### Mark Attendance
1. Login as Faculty
2. Create a Schedule
3. Go to Schedule and click "Mark Attendance"
4. Toggle Present/Absent for each student
5. Save Attendance

## Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: This deletes all data)
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

## Technical Stack

- **Backend:** Django 4.2.0
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Language:** Python 3.8+

## Browser Support

- Chrome (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)

## Future Enhancements

- [ ] Export attendance reports to PDF
- [ ] Email notifications for low attendance
- [ ] SMS alerts to students
- [ ] Attendance history graphs
- [ ] Leave management system
- [ ] Biometric/QR code integration
- [ ] Mobile app version

## Support & Contributions

For bugs, issues, or suggestions, please create an issue or contact the development team.

## License

This project is created for educational purposes.

---

**Created with ❤️ for College Attendance Management**
