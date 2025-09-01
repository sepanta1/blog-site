from django import forms
from .models import Contact,Newsletter

class Contact_form(forms.ModelForm):
   class Meta:
       model=Contact 
       fields='__all__'

class Newsletter_form(forms.ModelForm):
    class Meta:
        model=Newsletter
        fields='__all__'
