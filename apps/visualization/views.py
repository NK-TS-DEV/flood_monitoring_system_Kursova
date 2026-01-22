from django.shortcuts import render
from apps.Sensors.models import Sensor, SensorData
from apps.analysis.models import Alert
import json

def dashboard_view(request):

    sensors = Sensor.objects.all()


    active_alerts = Alert.objects.filter(is_active=True).order_by('-created_at')


    map_markers = []
    for sensor in sensors:
        latest_data = sensor.readings.first()
        value = latest_data.value if latest_data else "No Data"

        map_markers.append({
            'id': sensor.id,
            'name': f"{sensor.sensor_type} ({sensor.region})",
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
        'map_data_json': json.dumps(map_markers),
    }
    return render(request, 'dashboard.html', context)