from django.contrib import admin
from .models import Post,Category,Comment
# Register your models here.
admin.site.register(Category)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'counted_views', 'status', 'created_date']
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    search_fields = ['title', 'content']
    # ordering = ["created_date"]
@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display= ['name','parent_post','approved','created_date']
    date_hierarchy='created_date'
    empty_value_display='-empty-'
    search_fields=['name','parent_post']
    
    


