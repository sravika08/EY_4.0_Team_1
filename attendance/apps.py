"""
App configuration for the attendance application.
"""

from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    """Configuration class for the attendance app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
