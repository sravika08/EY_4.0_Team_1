"""
Views for the College Attendance Management System.
Handles authentication, dashboards, and attendance management for both students and faculty.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from functools import wraps

from .models import Student, Faculty, Schedule, Attendance, BRANCH_CHOICES, YEAR_CHOICES
from .forms import (
    StudentRegistrationForm, StudentLoginForm,
    FacultyRegistrationForm, FacultyLoginForm,
    UnifiedRegistrationForm, UnifiedLoginForm,
    ScheduleForm, AttendanceForm
)


# ============================================================================
# PERMISSION DECORATORS
# ============================================================================

def student_required(view_func):
    """
    Decorator to ensure only students can access the view.
    Redirects faculty and unauthenticated users to home page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('home')
        
        # Check if user is a student
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, 'This page is for students only.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def faculty_required(view_func):
    """
    Decorator to ensure only faculty can access the view.
    Redirects students and unauthenticated users to home page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('home')
        
        # Check if user is faculty
        if not hasattr(request.user, 'faculty_profile'):
            messages.error(request, 'This page is for faculty only.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


# ============================================================================
# HOME AND AUTHENTICATION VIEWS
# ============================================================================

def home(request):
    """
    Home page view that shows different content based on user type.
    Redirects authenticated users to their respective dashboards.
    """
    if request.user.is_authenticated:
        # Check if user is a student
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        # Check if user is faculty
        elif hasattr(request.user, 'faculty_profile'):
            return redirect('faculty_dashboard')
    
    return render(request, 'home.html')


# ============================================================================
# UNIFIED REGISTRATION AND LOGIN
# ============================================================================

def register(request):
    """
    Unified registration view for both students and faculty.
    Shows different form fields based on the selected role.
    """
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        elif hasattr(request.user, 'faculty_profile'):
            return redirect('faculty_dashboard')
    
    if request.method == 'POST':
        form = UnifiedRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                role = form.cleaned_data.get('role')
                messages.success(request, f'Registration as {role} successful! Please login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UnifiedRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Unified login view for both students and faculty.
    Authenticates user based on their role selection.
    """
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        elif hasattr(request.user, 'faculty_profile'):
            return redirect('faculty_dashboard')
    
    if request.method == 'POST':
        form = UnifiedLoginForm(request.POST)
        role = request.POST.get('role')
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Verify user role matches selected role
                if role == 'student':
                    if not hasattr(user, 'student_profile'):
                        messages.error(request, 'This account is not a student account. Please login as faculty.')
                        return render(request, 'login.html', {'form': form})
                elif role == 'faculty':
                    if not hasattr(user, 'faculty_profile'):
                        messages.error(request, 'This account is not a faculty account. Please login as student.')
                        return render(request, 'login.html', {'form': form})
                
                # Login successful
                login(request, user)
                if role == 'student':
                    messages.success(request, f'Welcome {user.student_profile.name}!')
                    return redirect('student_dashboard')
                else:
                    messages.success(request, f'Welcome {user.faculty_profile.name}!')
                    return redirect('faculty_dashboard')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UnifiedLoginForm()
    
    return render(request, 'login.html', {'form': form})


# Legacy student/faculty-specific registration and login views removed.
# Use the unified `register` and `login_view` views instead.


# ============================================================================
# LOGOUT VIEW
# ============================================================================

def user_logout(request):
    """
    View to handle user logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ============================================================================
# STUDENT DASHBOARD AND ATTENDANCE VIEWS
# ============================================================================

@student_required
def student_dashboard(request):
    """
    Student dashboard showing attendance overview (READ-ONLY).
    Displays:
    - Total classes attended
    - Total classes held
    - Attendance percentage
    - Predicted percentage if one more class is missed
    - Warning if attendance < 75%
    
    All calculations are done dynamically from the Attendance table.
    Note: This is a READ-ONLY view. Students cannot modify data.
    """
    # Get current student (decorator ensures user is authenticated student)
    
    student = request.user.student_profile
    
    # Get all attendance records for this student
    attendance_records = Attendance.objects.filter(student=student).select_related('schedule')
    
    # Calculate statistics dynamically
    total_classes = attendance_records.count()
    attended_classes = attendance_records.filter(status='P').count()
    absent_classes = attendance_records.filter(status='A').count()
    
    # Calculate attendance percentage
    if total_classes > 0:
        attendance_percentage = round((attended_classes / total_classes) * 100, 2)
    else:
        attendance_percentage = 0
    
    # Calculate percentage if one more class is missed
    if total_classes > 0:
        percentage_if_absent_one_more = round((attended_classes / (total_classes + 1)) * 100, 2)
    else:
        percentage_if_absent_one_more = 0
    
    # Check if attendance is below 75% (warning condition)
    is_below_threshold = attendance_percentage < 75
    
    # Get recent attendance records
    recent_attendances = attendance_records[:10]
    
    context = {
        'student': student,
        'total_classes': total_classes,
        'attended_classes': attended_classes,
        'absent_classes': absent_classes,
        'attendance_percentage': attendance_percentage,
        'percentage_if_absent_one_more': percentage_if_absent_one_more,
        'is_below_threshold': is_below_threshold,
        'recent_attendances': recent_attendances,
    }
    
    return render(request, 'student_dashboard.html', context)


@student_required
def student_attendance_details(request):
    """
    View for detailed attendance records of a student (READ-ONLY).
    Shows all classes with attendance status.
    Note: This is a READ-ONLY view. Students cannot modify data.
    """
    
    student = request.user.student_profile
    
    # Get all attendance records sorted by date (newest first)
    attendance_records = Attendance.objects.filter(
        student=student
    ).select_related('schedule', 'schedule__faculty').order_by('-schedule__date')
    
    # Calculate statistics
    total_classes = attendance_records.count()
    attended_classes = attendance_records.filter(status='P').count()
    absent_classes = total_classes - attended_classes
    
    if total_classes > 0:
        attendance_percentage = round((attended_classes / total_classes) * 100, 2)
    else:
        attendance_percentage = 0
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'total_classes': total_classes,
        'attended_classes': attended_classes,
        'absent_classes': absent_classes,
        'attendance_percentage': attendance_percentage,
    }
    
    return render(request, 'student_attendance_details.html', context)


# ============================================================================
# FACULTY DASHBOARD AND ATTENDANCE MARKING
# ============================================================================

@faculty_required
def faculty_dashboard(request):
    """
    Faculty dashboard showing schedules and attendance summary.
    Displays recent schedules and attendance statistics.
    """
    
    faculty = request.user.faculty_profile
    
    # Get recent schedules for this faculty
    recent_schedules = Schedule.objects.filter(faculty=faculty).order_by('-date')[:5]
    
    # Get attendance summary for students in the same branch and year
    students_in_batch = Student.objects.filter(
        branch=faculty.branch,
        year=faculty.year
    )
    
    # Calculate attendance summary for each student
    student_summaries = []
    for student in students_in_batch:
        attendance_records = Attendance.objects.filter(
            student=student,
            schedule__faculty=faculty
        )
        total = attendance_records.count()
        attended = attendance_records.filter(status='P').count()
        absent = total - attended
        
        if total > 0:
            percentage = round((attended / total) * 100, 2)
        else:
            percentage = 0
        
        student_summaries.append({
            'student': student,
            'total_classes': total,
            'attended_classes': attended,
            'absent_classes': absent,
            'percentage': percentage,
        })
    
    context = {
        'faculty': faculty,
        'recent_schedules': recent_schedules,
        'student_summaries': student_summaries,
        'total_students_in_batch': students_in_batch.count(),
    }
    
    return render(request, 'faculty_dashboard.html', context)


@faculty_required
def create_schedule(request):
    """
    View for faculty to create a new class schedule.
    Only faculty can create schedules.
    """
    
    faculty = request.user.faculty_profile
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.faculty = faculty
            schedule.save()
            messages.success(request, f'Class schedule created for {schedule.date}.')
            return redirect('faculty_dashboard')
    else:
        form = ScheduleForm()
    
    return render(request, 'create_schedule.html', {'form': form, 'faculty': faculty})


@faculty_required
def mark_attendance(request, schedule_id):
    """
    View for faculty to mark attendance for a specific class.
    Displays all students in the same branch and year.
    Only faculty can mark attendance.
    """
    
    faculty = request.user.faculty_profile
    schedule = get_object_or_404(Schedule, id=schedule_id, faculty=faculty)
    
    # Get all students in the same branch and year
    students = Student.objects.filter(
        branch=faculty.branch,
        year=faculty.year
    ).order_by('hall_ticket_id')
    
    if request.method == 'POST':
        form = AttendanceForm(students, request.POST)
        if form.is_valid():
            # Save attendance for each student
            for student in students:
                status = form.cleaned_data.get(f'student_{student.id}')
                # Create or update attendance record
                Attendance.objects.update_or_create(
                    student=student,
                    schedule=schedule,
                    defaults={'status': status}
                )
            
            messages.success(request, f'Attendance marked for {schedule.date}.')
            return redirect('faculty_dashboard')
    else:
        form = AttendanceForm(students)
    
    context = {
        'form': form,
        'schedule': schedule,
        'faculty': faculty,
        'students': students,
    }
    
    return render(request, 'mark_attendance.html', context)


@faculty_required
def view_all_schedules(request):
    """
    View for faculty to see all schedules and manage attendance.
    Only faculty can view and manage schedules.
    """
    
    faculty = request.user.faculty_profile
    schedules = Schedule.objects.filter(faculty=faculty).order_by('-date')
    
    context = {
        'schedules': schedules,
        'faculty': faculty,
    }
    
    return render(request, 'view_all_schedules.html', context)


@faculty_required
def view_student_list(request):
    """
    View for faculty to see all students in their batch.
    Allows filtering by branch and year.
    Only faculty can view student lists.
    """
    
    faculty = request.user.faculty_profile
    
    # Start with students in the same branch and year
    students = Student.objects.filter(
        branch=faculty.branch,
        year=faculty.year
    ).order_by('hall_ticket_id')
    
    # Calculate attendance for each student
    student_data = []
    for student in students:
        attendance_records = Attendance.objects.filter(
            student=student,
            schedule__faculty=faculty
        )
        total = attendance_records.count()
        attended = attendance_records.filter(status='P').count()
        absent = total - attended
        
        if total > 0:
            percentage = round((attended / total) * 100, 2)
        else:
            percentage = 0
        
        student_data.append({
            'student': student,
            'total_classes': total,
            'attended_classes': attended,
            'absent_classes': absent,
            'percentage': percentage,
        })
    
    context = {
        'faculty': faculty,
        'student_data': student_data,
    }
    
    return render(request, 'view_student_list.html', context)


# ============================================================================
# ERROR VIEWS
# ============================================================================

def page_not_found(request, exception):
    """Handle 404 errors."""
    return render(request, '404.html', status=404)


def server_error(request):
    """Handle 500 errors."""
    return render(request, '500.html', status=500)
