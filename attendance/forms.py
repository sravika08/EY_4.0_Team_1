"""
Forms for the College Attendance Management System.
Includes registration and login forms for both students and faculty.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student, Faculty, Schedule, Attendance, BRANCH_CHOICES, YEAR_CHOICES

# ============================================================================
# ROLE CHOICE
# ============================================================================

ROLE_CHOICES = [
    ('student', 'Student'),
    ('faculty', 'Faculty'),
]

# ============================================================================
# UNIFIED REGISTRATION FORM
# ============================================================================

class UnifiedRegistrationForm(forms.Form):
    """
    Unified registration form for both students and faculty.
    Displays different fields based on the selected role.
    """
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'onchange': 'toggleRegistrationFields(this.value)'
        }),
        label='Register as'
    )
    
    # Common fields
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    
    # Student-specific fields
    hall_ticket_id = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Hall Ticket ID'
        }),
        label='Hall Ticket ID'
    )
    student_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Full Name'
        }),
        label='Full Name'
    )
    student_branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Branch'
    )
    student_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Year'
    )
    
    # Faculty-specific fields
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        }),
        label='Username'
    )
    faculty_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Full Name'
        }),
        label='Full Name'
    )
    subject = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Subject'
        }),
        label='Subject'
    )
    faculty_branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Branch'
    )
    faculty_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Year'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            if len(password1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters long.')
        
        if role == 'student':
            # Validate student fields
            if not cleaned_data.get('hall_ticket_id'):
                raise forms.ValidationError('Hall Ticket ID is required for student registration.')
            if not cleaned_data.get('student_name'):
                raise forms.ValidationError('Name is required for student registration.')
            if not cleaned_data.get('student_branch'):
                raise forms.ValidationError('Branch is required for student registration.')
            if not cleaned_data.get('student_year'):
                raise forms.ValidationError('Year is required for student registration.')
            
            # Check if hall_ticket_id already exists
            if Student.objects.filter(hall_ticket_id=cleaned_data.get('hall_ticket_id')).exists():
                raise forms.ValidationError('This Hall Ticket ID is already registered.')
        
        elif role == 'faculty':
            # Validate faculty fields
            if not cleaned_data.get('username'):
                raise forms.ValidationError('Username is required for faculty registration.')
            if not cleaned_data.get('faculty_name'):
                raise forms.ValidationError('Name is required for faculty registration.')
            if not cleaned_data.get('subject'):
                raise forms.ValidationError('Subject is required for faculty registration.')
            if not cleaned_data.get('faculty_branch'):
                raise forms.ValidationError('Branch is required for faculty registration.')
            if not cleaned_data.get('faculty_year'):
                raise forms.ValidationError('Year is required for faculty registration.')
            
            # Check if username already exists
            if User.objects.filter(username=cleaned_data.get('username')).exists():
                raise forms.ValidationError('This username is already taken.')
        
        return cleaned_data
    
    def save(self):
        role = self.cleaned_data.get('role')
        
        if role == 'student':
            # Create student user and profile
            user = User.objects.create_user(
                username=self.cleaned_data.get('hall_ticket_id'),
                password=self.cleaned_data.get('password1')
            )
            Student.objects.create(
                user=user,
                hall_ticket_id=self.cleaned_data.get('hall_ticket_id'),
                name=self.cleaned_data.get('student_name'),
                branch=self.cleaned_data.get('student_branch'),
                year=int(self.cleaned_data.get('student_year'))
            )
            return user
        
        elif role == 'faculty':
            # Create faculty user and profile
            user = User.objects.create_user(
                username=self.cleaned_data.get('username'),
                password=self.cleaned_data.get('password1')
            )
            Faculty.objects.create(
                user=user,
                name=self.cleaned_data.get('faculty_name'),
                subject=self.cleaned_data.get('subject'),
                branch=self.cleaned_data.get('faculty_branch'),
                year=int(self.cleaned_data.get('faculty_year'))
            )
            return user

# ============================================================================
# UNIFIED LOGIN FORM
# ============================================================================

class UnifiedLoginForm(forms.Form):
    """
    Unified login form for both students and faculty.
    """
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'onchange': 'toggleLoginFields(this.value)'
        }),
        label='Login as'
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Hall Ticket ID / Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )



class StudentRegistrationForm(UserCreationForm):
    """
    Form for student registration.
    Creates a new Student account with hall_ticket_id and password.
    """
    hall_ticket_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Hall Ticket ID'
        }),
        label='Hall Ticket ID'
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Full Name'
        })
    )
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('hall_ticket_id', 'name', 'branch', 'year', 'password1', 'password2')

    def clean_hall_ticket_id(self):
        """Validate that hall_ticket_id is unique."""
        hall_ticket_id = self.cleaned_data.get('hall_ticket_id')
        if Student.objects.filter(hall_ticket_id=hall_ticket_id).exists():
            raise forms.ValidationError('This Hall Ticket ID is already registered.')
        return hall_ticket_id

    def save(self, commit=True):
        """Create both User and Student objects."""
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('hall_ticket_id')
        
        if commit:
            user.save()
            # Create Student profile
            Student.objects.create(
                user=user,
                hall_ticket_id=self.cleaned_data.get('hall_ticket_id'),
                name=self.cleaned_data.get('name'),
                branch=self.cleaned_data.get('branch'),
                year=int(self.cleaned_data.get('year'))
            )
        return user


class StudentLoginForm(AuthenticationForm):
    """
    Form for student login using hall_ticket_id and password.
    """
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Hall Ticket ID'
        }),
        label='Hall Ticket ID'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )


# ============================================================================
# FACULTY FORMS
# ============================================================================

class FacultyRegistrationForm(UserCreationForm):
    """
    Form for faculty registration.
    Creates a new Faculty account with username and password.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Full Name'
        })
    )
    subject = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Subject'
        })
    )
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'name', 'subject', 'branch', 'year', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })
        self.fields['username'].label = 'Username'

    def save(self, commit=True):
        """Create both User and Faculty objects."""
        user = super().save(commit=False)
        
        if commit:
            user.save()
            # Create Faculty profile
            Faculty.objects.create(
                user=user,
                name=self.cleaned_data.get('name'),
                subject=self.cleaned_data.get('subject'),
                branch=self.cleaned_data.get('branch'),
                year=int(self.cleaned_data.get('year'))
            )
        return user


class FacultyLoginForm(AuthenticationForm):
    """
    Form for faculty login using username and password.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )


# ============================================================================
# SCHEDULE AND ATTENDANCE FORMS
# ============================================================================

class ScheduleForm(forms.ModelForm):
    """
    Form for faculty to create class schedules.
    """
    class Meta:
        model = Schedule
        fields = ('date', 'subject', 'topic')
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Subject'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Topic'
            }),
        }


class AttendanceForm(forms.Form):
    """
    Form for marking attendance for multiple students.
    Generates attendance fields dynamically for each student.
    """
    def __init__(self, students, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically create fields for each student
        for student in students:
            self.fields[f'student_{student.id}'] = forms.ChoiceField(
                choices=[('P', 'Present'), ('A', 'Absent')],
                required=True,
                widget=forms.RadioSelect(attrs={
                    'class': 'attendance-radio'
                }),
                label=f"{student.hall_ticket_id} - {student.name}"
            )
