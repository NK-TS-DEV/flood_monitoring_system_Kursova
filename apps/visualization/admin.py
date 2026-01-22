from django.contrib import admin
from .models import MapSettings

@admin.register(MapSettings)
class MapSettingsAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'default_lat', 'default_lon', 'default_zoom')


    def has_delete_permission(self, request, obj=None):
        return False


    def has_add_permission(self, request):
        return not MapSettings.objects.exists()