"""
URL configuration for the attendance app.
Defines all routes for authentication and dashboards.
"""

from django.urls import path
from . import views

# URL patterns for the attendance management system
urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    
    # Unified authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    
    # Legacy student/faculty-specific auth routes removed — use unified 'register' and 'login'
    
    # Student views
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/attendance/details/', views.student_attendance_details, name='student_attendance_details'),
    
    # Faculty views
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/schedule/create/', views.create_schedule, name='create_schedule'),
    path('faculty/schedule/all/', views.view_all_schedules, name='view_all_schedules'),
    path('faculty/attendance/mark/<int:schedule_id>/', views.mark_attendance, name='mark_attendance'),
    path('faculty/students/', views.view_student_list, name='view_student_list'),
]
