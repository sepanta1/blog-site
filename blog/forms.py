from django import forms
from .models import Comment

class Comments_form(forms.ModelForm):
    """
    Form for submitting comments on blog posts.
    
    Allows users to provide their name, email, subject, and associate the comment
    with a specific parent post.
    """
    class Meta:
        model=Comment
        fields=['parent_post','name','email','subject']