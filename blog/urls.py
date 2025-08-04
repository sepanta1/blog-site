from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('blog-home/', views.blog_home, name='blog-home'),
    path('<int:pid>/', views.blog_single, name='blog-single'),
    path('category/<str:cat_name>',views.category_link, name='cat_link')
]
