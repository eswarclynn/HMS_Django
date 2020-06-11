from django import forms

from institute.models import  Institutestd

class PostForm(forms.ModelForm):

    class Meta:
        model = Institutestd
        fields = ('photo','application','undertake','recipt','afd',)