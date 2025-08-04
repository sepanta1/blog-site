from django.contrib import admin
from .models import Post,Contact,Category
# Register your models here.
admin.site.register(Category)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'counted_views', 'status', 'created_date']
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    search_fields = ['title', 'content']
    # ordering = ["created_date"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'created_date']
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    search_fields = ['name', 'email','subject']
