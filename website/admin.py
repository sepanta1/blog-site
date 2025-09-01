from django.contrib import admin
from .models import Contact,Newsletter


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'created_date']
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    search_fields = ['name', 'email','subject']
    
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display=['email','created_date']
    empty_value_display = "-empty-"
    search_fields=['email']
    date_hierarchy = 'created_date'