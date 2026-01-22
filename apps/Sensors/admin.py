from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Sensor, SensorData, AdminUser

class SensorDataInline(admin.TabularInline):
    """
    Позволяет видеть последние измерения прямо внутри страницы Сенсора.
    """
    model = SensorData
    readonly_fields = ('timestamp', 'value')
    extra = 0 #
    can_delete = False
    max_num = 10 #
    ordering = ['-timestamp']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sensor_type', 'region', 'status', 'owner_link')
    list_filter = ('status', 'sensor_type', 'region')
    search_fields = ('region', 'id')
    inlines = [SensorDataInline] #


    def owner_link(self, obj):
        return obj.owner.username if obj.owner else "-"
    owner_link.short_description = 'Owner'

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    """
    Отдельный список для всех данных (полезно для проверки).
    """
    list_display = ('sensor', 'value', 'timestamp')
    list_filter = ('sensor__sensor_type', 'timestamp')
    list_per_page = 50

@admin.register(AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    """
    Админка для нашего специального класса AdminUser.
    """
    list_display = ('username', 'email', 'is_staff', 'last_login')
    fieldsets = BaseUserAdmin.fieldsets