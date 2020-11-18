from django import forms
from institute.models import Student
from .models import Complaint, MedicalIssue

class ComplaintCreationForm(forms.ModelForm):
    complainee_id = forms.IntegerField(required=False, help_text='Only for Indisciplinary, Discrimination/Harassment or Damage to property complaints.')
    class Meta:
        model = Complaint
        fields = ['type', 'complainee_id', 'summary', 'detailed']

        labels = {
            'detailed': 'Details'
        }
        
        widgets = {
            'detailed': forms.Textarea(attrs={'rows': 4})
        }

    def clean_complainee_id(self):
        complainee_id = self.cleaned_data.get('complainee_id')
        if complainee_id and not Student.objects.filter(regd_no=complainee_id).exists():
            raise forms.ValidationError("Invalid registration number.")
        return complainee_id

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        complainee_id = cleaned_data.get('complainee_id')

        if (type == 'Indisciplinary' or type == 'Discrimination/ Harassment' or type == 'Damage to property') and not complainee_id:
            raise forms.ValidationError("Please specify the registration no. of the person against whom the complaint has to be registered.")
        elif not (type == 'Indisciplinary' or type == 'Discrimination/ Harassment' or type == 'Damage to property') and complainee_id:
            raise forms.ValidationError("Cannot assign complainee to {} complaint.".format(type))
        
        return cleaned_data

class ComplaintUpdationForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['status', 'remark', ]

        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4})
        }

class MedicalIssueUpdationForm(forms.ModelForm):
    class Meta:
        model = MedicalIssue
        fields = ['status', 'remark', ]

        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4})
        }