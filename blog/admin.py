from django.contrib import admin

from .models import Category, Comment, Contact, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject"]
    list_filter = ["name", "subject"]
    search_fields = ["name", "email", "subject"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "get_categories",
        "created_date",
        "status",
    ]
    list_filter = ["status", "author", "category"]
    list_editable = [
        "status",
    ]
    empty_value_display = "-empty-"
    search_fields = [
        "title",
    ]

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_date",
        "approved",
    ]
    list_filter = ["approved", "created_date"]
    list_editable = [
        "approved",
    ]
    search_fields = ["name", "parent_post"]
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
