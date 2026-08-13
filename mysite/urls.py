from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from blog.sitemaps import BlogSitemap
# Import custom sitemap classes
from website.sitemaps import StaticViewSitemap
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),

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
    path("api/v1/", include("blog.api_urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/v1/dj-rest-auth/registration/",
         include("dj_rest_auth.registration.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(
        url_name="schema"), name="redoc",),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(
        url_name="schema"), name="swagger-ui"),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if 'debug_toolbar' in settings.INSTALLED_APPS:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
