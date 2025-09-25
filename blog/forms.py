from django import forms
from .models import Comments

class Comments_form(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['parent_post','name','email','subject']