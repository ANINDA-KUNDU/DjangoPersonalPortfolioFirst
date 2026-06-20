from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

from cloudinary.models import CloudinaryField
# Create your models here.

class Work( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    title = models.CharField( max_length = 255 )
    description = models.TextField( max_length = 700 )
    picture = CloudinaryField( resource_type = "image", folder = "core/work", default = "core/work/default_work.png", use_filename = True, unique_filename = False,  blank = True, null = True )
    created_at = models.DateTimeField( auto_now_add = True )
    modified_at = models.DateTimeField( auto_now = True )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Work"
        
    def get_absolute_url(self):
        return reverse("work")

class Visitor(models.Model):
    session_key = models.CharField( max_length = 255, blank = True, null = True )
    fingerprint = models.CharField( max_length = 255, db_index = True )
    ip_address = models.GenericIPAddressField( null = True, blank = True )
    browser = models.CharField( max_length = 100, null = True )
    browser_version = models.CharField( max_length = 100, blank = True )
    os_name = models.CharField( max_length = 255, blank = True )
    os_version = models.CharField( max_length = 100, blank = True )
    device_name = models.CharField( max_length = 100, blank = True )
    is_mobile = models.BooleanField( default = False )
    is_tablet = models.BooleanField( default = False )
    is_pc = models.BooleanField( default = False )
    is_bot = models.BooleanField( default = False )
    path = models.CharField( max_length = 500 )
    referrer = models.URLField( blank = True, null = True )
    user_agent = models.TextField( blank = True )
    visit_count = models.PositiveIntegerField( default = 1 )
    first_visit = models.DateTimeField( auto_now_add = True )
    last_visit = models.DateTimeField( auto_now = True )
    
    class Meta:
        ordering = ["-last_visit"]
    
    def __str__(self):
        return f"{self.ip_address}({self.visit_count})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["fingerprint", "path"],
                name = "unique_visitor_page"
            )
        ]
    
    class Meta:
        verbose_name_plural = 'Visitor'