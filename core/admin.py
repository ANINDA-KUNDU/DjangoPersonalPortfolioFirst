from django.contrib import admin
from .models import Work, Visitor
# Register your models here.

admin.site.register( Work )

@admin.register( Visitor )
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "browser", "os_name", "device_name", "visit_count", "last_visit",)
    search_fields = ("ip_address", "browser", "os_name")
    list_filter = ("browser", "os_name", "is_mobile", "is_tablet", "is_pc",)
    readonly_fields = ("first_visit", "last_visit",)