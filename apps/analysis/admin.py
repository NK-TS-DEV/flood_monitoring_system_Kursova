from django.contrib import admin
from .models import AnalysisRule, Alert

@admin.register(AnalysisRule)
class AnalysisRuleAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'warning_threshold', 'critical_threshold')
    list_editable = ('warning_threshold', 'critical_threshold')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'level', 'created_at', 'is_active')
    list_filter = ('is_active', 'level', 'created_at')
    readonly_fields = ('created_at',)
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} alerts were marked as resolved.")
    mark_as_resolved.short_description = "Deactivate selected alerts"