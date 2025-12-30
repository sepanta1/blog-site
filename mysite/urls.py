"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Key features included:
- Admin interface
- Main website, blog, and accounts apps
- Sitemap for SEO (static pages + blog posts)
- Robots.txt handling
- CAPTCHA integration
- TinyMCE rich text editor URLs
- Serving static and media files during development
- Django Debug Toolbar (development only)

"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

# Import custom sitemap classes
from website.sitemaps import StaticViewSitemap
from blog.sitemaps import BlogSitemap

# Import debug toolbar URLs (only active in DEBUG mode)
from debug_toolbar.toolbar import debug_toolbar_urls

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    # robots module
    path('robots.txt', include('robots.urls')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # captcha module
    path('captcha/', include('captcha.urls')),
    # tinymce editor module
    path('tinymce/', include('tinymce.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()
