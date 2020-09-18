from django import forms
from institute.models import Student
from .models import Complaint

class ComplaintCreationForm(forms.ModelForm):
    complainee_id = forms.IntegerField(required=False)
    class Meta:
        model = Complaint
        fields = ['type', 'complainee_id', 'summary', 'detailed']
        
        widgets = {
            'detailed': forms.Textarea(attrs={'rows': 4})
        }

    def clean_complainee_id(self):
        complainee_id = self.cleaned_data.get('complainee_id')
        if complainee_id and not Student.objects.filter(regd_no=complainee_id).exists():
            raise forms.ValidationError("Invalid registration number.")
        return complainee_id

class ComplaintUpdationForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['status', 'remark', ]

        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4})
        }