from django.contrib import admin
from django.urls import path, include  # 1. Добавь include

from apps.visualization.views import dashboard_view
from apps.Sensors.views import sensor_list_view, sensor_create_view, sensor_delete_view
from apps.notifications.views import subscribe_view
from apps.reports.views import analytics_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', dashboard_view, name='dashboard'),
    path('sensors/', sensor_list_view, name='sensor_list'),
    path('sensors/add/', sensor_create_view, name='sensor_add'),
    path('sensors/delete/<int:pk>/', sensor_delete_view, name='sensor_delete'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('analytics/', analytics_view, name='analytics'),
]