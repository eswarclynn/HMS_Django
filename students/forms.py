from django import forms
from django.utils import timezone
from .models import Outing

class OutingForm(forms.ModelForm):
    class Meta:
        model = Outing
        fields = ['fromDate', 'toDate', 'purpose']

        labels = {
            'fromDate': 'From Date & Time',
            'toDate': 'To Date & Time'
        }

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        from_date = cleaned_data.get('fromDate')
        to_date = cleaned_data.get('toDate')

        if from_date and to_date and (from_date >= to_date):
            raise forms.ValidationError("To Date and Time should be later than From Date and Time")

        return cleaned_data

    def clean_fromDate(self):
        from_date = self.cleaned_data.get('fromDate')
        print(self.cleaned_data)
        if from_date <= timezone.now():
            raise forms.ValidationError("From Date should be later than the moment!")
        return from_date
