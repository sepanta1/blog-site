
# Import debug toolbar URLs (only active in DEBUG mode)
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import BlogSitemap

# Import custom sitemap classes
from website.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
    path("api/v1/", include("blog.api_urls")),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
    # robots module
    path("robots.txt", include("robots.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # captcha module
    path("captcha/", include("captcha.urls")),
    # tinymce editor module
    path("tinymce/", include("tinymce.urls")),
    # api v1
    path("api/v1/", include("blog.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()
