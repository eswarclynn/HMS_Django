from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from institute.models import Student, Official
from workers.models import Worker

class SignUpForm(UserCreationForm):
    entity_id = forms.CharField(label='Registration No./Staff ID')
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'is_student', 'is_official', 'is_worker')
        
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
        labels = {
            'is_student': 'Student',
            'is_official': 'Official',
            'is_worker': 'Worker'
        }

    def clean(self):
        cleaned_data = super().clean()
        is_student = cleaned_data.get('is_student')
        is_official = cleaned_data.get('is_official')
        is_worker = cleaned_data.get('is_worker')
        email = cleaned_data.get('email')

        if not(is_student or is_official or is_worker):
            raise forms.ValidationError('User should belong to a single type.')

        if (is_student and is_official) or (is_student and is_worker) or (is_worker and is_official):
            raise forms.ValidationError('User cannot be of more than one type.')

        if is_student and (not email.endswith('@student.nitandhra.ac.in')):
            raise forms.ValidationError('Students should use institute eMail ID')

        if (is_worker or is_official) and (not email.endswith('@nitandhra.ac.in')):
            raise forms.ValidationError('Staff should use institute eMail ID')

        if not ((is_student and Student.objects.filter(regd_no = entity_id).exists()) or (is_official and Official.objects.filter(emp_id = entity_id).exists()) or  (is_worker and Worker.objects.filter(staff_id = entity_id).exists())):
            if is_student:
                user_type = 'Student'
            elif is_official or is_worker:
                user_type = 'Staff'

            raise forms.ValidationError(user_type + " doesn't exist in database. Please contact admin.")
                
        return cleaned_data

