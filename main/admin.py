from django.contrib import admin
from .models import APKVersion

# Register your models here.
class APKVersionAdmin(admin.ModelAdmin):
    list_display = ('version_code', 'version_name', 'release_date', 'download_url')
    search_fields = ('version_name',)
    
admin.site.register(APKVersion, APKVersionAdmin)