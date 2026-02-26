"""
Django admin configuration for the attendance app.
Registers all models for admin panel management.
"""

from django.contrib import admin
from .models import Student, Faculty, Schedule, Attendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin configuration for Student model."""
    list_display = ('hall_ticket_id', 'name', 'branch', 'year', 'created_at')
    list_filter = ('branch', 'year', 'created_at')
    search_fields = ('hall_ticket_id', 'name', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('hall_ticket_id', 'name', 'branch', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin configuration for Faculty model."""
    list_display = ('name', 'subject', 'branch', 'year', 'created_at')
    list_filter = ('branch', 'year', 'created_at')
    search_fields = ('name', 'subject', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('name', 'subject', 'branch', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Admin configuration for Schedule model."""
    list_display = ('faculty', 'date', 'subject', 'topic', 'created_at')
    list_filter = ('date', 'faculty', 'created_at')
    search_fields = ('subject', 'topic', 'faculty__name')
    ordering = ('-date',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'

    fieldsets = (
        ('Class Information', {
            'fields': ('faculty', 'date', 'subject', 'topic')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin configuration for Attendance model."""
    list_display = ('student', 'schedule', 'status', 'marked_at')
    list_filter = ('status', 'marked_at', 'schedule__date')
    search_fields = ('student__hall_ticket_id', 'student__name', 'schedule__subject')
    ordering = ('-marked_at',)
    readonly_fields = ('marked_at', 'updated_at')
    date_hierarchy = 'marked_at'

    fieldsets = (
        ('Attendance Information', {
            'fields': ('student', 'schedule', 'status')
        }),
        ('Timestamps', {
            'fields': ('marked_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
