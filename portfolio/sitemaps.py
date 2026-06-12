from django.contrib.sitemaps import Sitemap
from core.models import Work

class WorkSitemap(Sitemap):
    def items(self):
        return Work.objects.all()
    
    def lastmod(self, obj):
        return obj.modified_at