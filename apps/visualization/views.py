from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from apps.Sensors.models import Sensor, SensorData
from apps.analysis.models import Alert
import json

def dashboard_view(request):
    # 1. Отримуємо всі сенсори
    sensors = Sensor.objects.all()

    # 2. Отримуємо активні тривоги
    active_alerts = Alert.objects.filter(is_active=True).order_by('-created_at')

    # 3. Готуємо дані для JS карти (MapService logic)
    map_markers = []
    for sensor in sensors:
        # Отримуємо останнє значення
        latest_data = sensor.data.last()
        value = latest_data.value if latest_data else "Немає даних"

        map_markers.append({
            'id': sensor.sensor_id,
            'name': sensor.name,
            'lat': sensor.latitude,
            'lng': sensor.longitude,
            'status': sensor.status,
            'val': value,
            'region': sensor.region
        })

    context = {
        'sensors_count': sensors.count(),
        'alerts_count': active_alerts.count(),
        'alerts': active_alerts,
        'map_data_json': json.dumps(map_markers), # Передаємо як JSON для JS
    }
    return render(request, 'dashboard.html', context)