# Getting Started Guide

## Quick Start (5 Minutes)

### For Windows Users:
1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```
   cd path\to\edunetfinal
   ```
3. Run the setup script:
   ```
   .\setup.bat
   ```
4. Follow the prompts to create an admin account
5. Open browser and go to: `http://127.0.0.1:8000`

### For macOS/Linux Users:
1. Open Terminal
2. Navigate to the project directory:
   ```
   cd path/to/edunetfinal
   ```
3. Run the setup script:
   ```
   bash setup.sh
   ```
4. Follow the prompts to create an admin account
5. Open browser and go to: `http://127.0.0.1:8000`

---

## Manual Setup

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User
```bash
python manage.py createsuperuser
```
Enter: username, email, password (confirm)

### Step 5: Run Development Server
```bash
python manage.py runserver
```

### Step 6: Access Application
- Main App: http://127.0.0.1:8000
- Admin Panel: http://127.0.0.1:8000/admin

---

## First Time Login

### Create Test Accounts from Admin Panel

1. Go to: `http://127.0.0.1:8000/admin`
2. Login with superuser credentials
3. You can manage everything from here

### Or Use the Web Interface

#### Register a Student:
1. Go to Home Page
2. Click "Student Portal" → "Register"
3. Fill in details:
   - Hall Ticket ID: `CSE001`
   - Name: `John Doe`
   - Branch: `CSE`
   - Year: `3rd Year`
   - Password: `Test@1234`
4. Click Register and then login

#### Register Faculty:
1. Go to Home Page
2. Click "Faculty Portal" → "Register"
3. Fill in details:
   - Username: `prof_smith`
   - Name: `Prof. Smith`
   - Subject: `Data Structures`
   - Branch: `CSE`
   - Year: `3rd Year`
   - Password: `Prof@1234`
4. Click Register and then login

---

## How to Use

### As a Student:

1. **Login**
   - Enter Hall Ticket ID and password

2. **View Dashboard**
   - See attendance percentage
   - View total/attended/absent classes
   - Check warning if below 75%
   - See prediction for missing one more class

3. **View Detailed Attendance**
   - Click "My Attendance"
   - See all attendance records with dates and subjects
   - Track attendance trends

### As Faculty:

1. **Login**
   - Enter username and password

2. **Create Schedule**
   - Click "Create Schedule"
   - Enter date, subject, and topic
   - Click "Create Schedule"

3. **Mark Attendance**
   - Go to "Schedules"
   - Click "Mark Attendance" on a schedule
   - Toggle Present/Absent for each student
   - Save Attendance

4. **View Student List**
   - Click "Students"
   - See all students in your batch
   - View attendance percentage for each student
   - Monitor attendance trends

---

## Troubleshooting

### Issue: "Port 8000 already in use"

**Solution:**
```bash
python manage.py runserver 8001
```

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "No database tables"

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: Can't login with created account

**Solution:**
- Make sure you have logged in first
- Check that the password is correct
- Ensure the account exists (check admin panel)

---

## Key Features to Try

### 1. Create a Complete Workflow

**Step 1:** Register as Student
- Create account with valid details

**Step 2:** Register as Faculty
- Create account for same branch/year

**Step 3:** Create Schedule
- Login as faculty
- Create a class schedule

**Step 4:** Mark Attendance
- Click on schedule
- Mark students present/absent
- Save

**Step 5:** View Attendance
- Login as student
- Go to dashboard
- See updated attendance

### 2. Test Attendance Calculation

- View student dashboard
- Current attendance percentage updates
- Prediction shows impact of missing one more class
- Warning appears if below 75%

### 3. Admin Panel Features

- Login at `/admin`
- Manage all users, students, faculty
- Create/edit schedules
- View/modify attendance records
- See detailed information about each model

---

## Common Test Scenarios

### Scenario 1: Create Test Data

1. Create Faculty: Prof Wang
   - Subject: Python Programming
   - Branch: IT
   - Year: 2nd Year

2. Create Students in IT-2nd Year:
   - Student 1: `IT004` - Jane Smith
   - Student 2: `IT005` - Bob Johnson

3. Create Schedules:
   - Date: Today
   - Subject: Python Programming
   - Topic: Functions and Modules

4. Mark Attendance:
   - Student 1: Present
   - Student 2: Absent

5. Check Results:
   - Student 1: 100% attendance (1/1)
   - Student 2: 0% attendance (0/1)

### Scenario 2: Test Threshold Warning

1. Create Schedule and mark several attendances
2. Mark student absent multiple times
3. Check dashboard when attendance < 75%
4. Red warning should appear

### Scenario 3: Test Predictions

1. Ensure attendance is at least 75%
2. View dashboard
3. Note current percentage
4. Check "If you miss one more class" section
5. Verify calculation is correct

---

## File Locations

- **Database:** `db.sqlite3` (in root directory)
- **Templates:** `templates/` folder
- **Static Files:** `static/` folder
- **Models:** `attendance/models.py`
- **Views:** `attendance/views.py`
- **URLs:** `attendance/urls.py`
- **Forms:** `attendance/forms.py`

---

## Environment Variables

Default configuration uses:
- **Database:** SQLite3 (`db.sqlite3`)
- **Debug Mode:** On (Change in `settings.py` for production)
- **Allowed Hosts:** All (`*`)

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Use a proper database (PostgreSQL, MySQL)
4. Set a strong SECRET_KEY

---

## Useful Django Commands

```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Admin panel
python manage.py createsuperuser
python manage.py changepassword username

# Check system
python manage.py check

# Collect static files
python manage.py collectstatic

# Database backup
python manage.py dumpdata > backup.json
```

---

## Need More Help?

- Check the README.md for detailed documentation
- Review the Django models in `attendance/models.py`
- Check views in `attendance/views.py`
- Visit Django docs: https://docs.djangoproject.com

---

**Happy Learning! 🎓**
