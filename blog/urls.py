from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('blog-home/', views.blog_home, name='blog-home'),
    path('<int:pid>/', views.blog_single, name='blog-single'),
    path('category/<str:cat_name>',views.blog_home, name='cat_link'),
    path('author/<str:author_name>',views.blog_home,name='author_name'),
    path('search/',views.blog_search,name='search'),
    path('test/',views.test,name='test'),
    
]
