from django.apps import apps
from .models import MapSettings

class MapService:
    """
    Реализация логики MapService из UML.
    Отвечает за подготовку данных для отображения на карте.
    """

    def __init__(self):

        self.settings = MapSettings.objects.first()
        if not self.settings:
            self.settings = MapSettings.objects.create()

    def get_map_config(self):
        """Возвращает ключи и настройки провайдера"""
        return {
            'provider': self.settings.provider_name,
            'api_key': self.settings.api_key,
            'center': [self.settings.default_lat, self.settings.default_lon],
            'zoom': self.settings.default_zoom
        }

    def get_markers(self):
        """
        Аналог атрибута markers: list из UML.
        Собирает все сенсоры и превращает их в формат для JS карт.
        """
        Sensor = apps.get_model('Sensors', 'Sensor')
        sensors = Sensor.objects.all()

        markers_data = []
        for sensor in sensors:

            markers_data.append(self.add_sensor_marker(sensor))

        return markers_data

    @staticmethod
    def add_sensor_marker(sensor):
        """
        Метод из UML: add_sensor_marker(sensor)
        Превращает объект Sensor в словарь данных для маркера.
        """
        latest_data = sensor.get_latest_data()
        value_str = f"{latest_data.value}" if latest_data else "No Data"

        return {
            'id': sensor.id,
            'lat': sensor.latitude,
            'lon': sensor.longitude,
            'type': sensor.sensor_type,
            'status': sensor.status,
            'popup_text': f"<b>{sensor.region}</b><br>Value: {value_str}"
        }

    @staticmethod
    def get_current_alerts():
        """
        Метод из UML: get_current_alerts()
        Возвращает список активных зон тревоги.
        """
        Alert = apps.get_model('analysis', 'Alert')
        active_alerts = Alert.objects.filter(is_active=True)

        alert_zones = []
        for alert in active_alerts:
            alert_zones.append({
                'sensor_id': alert.sensor.id,
                'level': alert.level, # 'warning' or 'critical'
                'lat': alert.sensor.latitude,
                'lon': alert.sensor.longitude,
                'message': alert.message
            })
        return alert_zones

    @staticmethod
    def update_sensor_status(sensor, status):
        """
        Метод из UML: update_sensor_status()
        """
        sensor.status = status
        sensor.save()
        return True