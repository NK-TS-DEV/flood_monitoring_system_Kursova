from .models import Alert, AnalysisRule
from apps.Sensors.models import SensorData

class Analyzer:
    """
    Реализация класса Analyzer из UML.
    Отвечает за бизнес-логику проверки данных.
    """

    def analyze(self, sensor_data: SensorData):
        """
        Метод из UML: analyze()
        Проверяет входящие данные на соответствие правилам.
        """

        try:
            rule = AnalysisRule.objects.get(sensor_type=sensor_data.sensor.sensor_type)
        except AnalysisRule.DoesNotExist:

            return None


        alert_level = None

        if sensor_data.value >= rule.critical_threshold:
            alert_level = 'critical'
        elif sensor_data.value >= rule.warning_threshold:
            alert_level = 'warning'


        if alert_level:
            return self.generate_alert(sensor_data, alert_level)

        return None

    @staticmethod
    def generate_alert( sensor_data: SensorData, level: str):
        """
        Метод из UML: generate_alert(sensor, data)
        Создает запись в таблице Alert.
        """

        existing_alert = Alert.objects.filter(
            sensor=sensor_data.sensor,
            level=level,
            is_active=True
        ).exists()

        if existing_alert:
            return None

        message = (
            f"Alert triggered for {sensor_data.sensor.region}. "
            f"Current value: {sensor_data.value}. Threshold exceeded."
        )

        new_alert = Alert.objects.create(
            sensor=sensor_data.sensor,
            triggering_data=sensor_data,
            level=level,
            message=message,
            is_active=True
        )

        return new_alert

    def process_data(self, data: SensorData):
        """
        Метод из UML: process_data(data)
        Главная точка входа.
        """
        return self.analyze(data)