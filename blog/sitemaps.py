from django.contrib.sitemaps import Sitemap
from blog.models import Post


class BlogSitemap(Sitemap):
    """
    Sitemap class for blog posts to help search engines discover and index published content.

    Includes only published posts (status=True), sets a weekly change frequency,
    and assigns a moderate priority of 0.5.
    """
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        """Returns a queryset of published Post objects to be included in the sitemap."""
        return Post.objects.filter(status=True)

    def lastmod(self, obj):
        """
        Returns the last modification date for a given Post object.

        Used by search engines to determine when the content was last updated.
        """
        return obj.published_date
