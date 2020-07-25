from django import forms
from institute.models import Institutestd, Officials


class StudentForm(forms.ModelForm):
    pwd = forms.ChoiceField(
        choices=((True, 'Yes'), (False, 'No')), 
        label='Person with Disability',
    )
    is_hosteller = forms.ChoiceField(
        choices=((True, 'Hosteller'), (False, 'Day Scholar')), 
        label='Hosteller/Day Scholar' 
    )
    has_paid = forms.ChoiceField(
        choices=( (False, 'No'), (True, 'Yes')), 
        label='Paid Hostel Fee',
    )

    class Meta:
        model = Institutestd
        fields = '__all__'

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'dop': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 8}),
        }

        labels = {
            'regd_no': 'Registration No.',
            'dob': 'Date of Birth',
            'dop': 'Date of Payment',
        }
