"""
Models for the College Attendance Management System.
This module contains all database models for managing students, faculty, 
schedules, and attendance records.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Choice tuples for branches and years
BRANCH_CHOICES = [
    ('CSE', 'Computer Science & Engineering'),
    ('ECE', 'Electronics & Communication Engineering'),
    ('IT', 'Information Technology'),
    ('ME', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
]

YEAR_CHOICES = [
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
]

ATTENDANCE_STATUS_CHOICES = [
    ('P', 'Present'),
    ('A', 'Absent'),
]


class Student(models.Model):
    """
    Student model linked to Django's User model.
    Stores student-specific information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    hall_ticket_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['hall_ticket_id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        """Return a string representation of the student."""
        return f"{self.hall_ticket_id} - {self.name}"


class Faculty(models.Model):
    """
    Faculty model linked to Django's User model.
    Stores faculty-specific information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculty'

    def __str__(self):
        """Return a string representation of the faculty member."""
        return f"{self.name} - {self.subject}"


class Schedule(models.Model):
    """
    Schedule model for storing class schedules.
    Links faculty, date, subject, and topic information.
    """
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField(db_index=True)
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('faculty', 'date')  # No duplicate classes for same faculty on same day
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        """Return a string representation of the schedule."""
        return f"{self.faculty.name} - {self.date} - {self.subject}"


class Attendance(models.Model):
    """
    Attendance model for recording student attendance.
    Links student and schedule records with attendance status.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS_CHOICES, default='A')
    marked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'schedule')  # One attendance record per student per class
        ordering = ['-marked_at']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['student', 'schedule']),
            models.Index(fields=['student', '-marked_at']),
        ]

    def __str__(self):
        """Return a string representation of the attendance record."""
        return f"{self.student.hall_ticket_id} - {self.schedule.date} - {self.get_status_display()}"
