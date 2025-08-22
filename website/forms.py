from django import forms
from .models import Contact

class Contact_form(forms.ModelForm):
   class Meta:
       model=Contact 
       fields='__all__'