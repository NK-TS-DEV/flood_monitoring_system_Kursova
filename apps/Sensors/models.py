from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps

class Sensor(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensors'
    )
    region = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def collect_data(self, value: float):
        """
        Создает новую запись данных для этого датчика.
        В реальной системе здесь мог бы быть запрос к API устройства,
        но в рамках системы мы просто сохраняем переданное значение.
        """
        new_data = SensorData.objects.create(sensor=self, value=value)
        return new_data

    def get_status(self):
        return self.get_status_display()

    def get_latest_data(self):
        """
        Возвращает последнее измерение.
        Благодаря ordering = ['-timestamp'] в SensorData, first() вернет самое свежее.
        """
        return self.readings.first()

    def get_data_history(self, start_date, end_date):
        """
        Возвращает QuerySet (список) измерений за период.
        Используем self.readings, так как в SensorData указан related_name='readings'.
        """
        return self.readings.filter(timestamp__range=(start_date, end_date))

    def __str__(self):
        return f"Sensor {self.id} ({self.sensor_type}) - {self.region}"


class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(help_text="Recorded value")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.sensor_type} @ {self.timestamp.strftime('%H:%M')}: {self.value}"

    def is_critical(self):
        """
        Простая проверка. В будущем можно связать это с таблицей правил (AnalysisRule).
        Пока сделаем 'хардкод' для примера.
        """

        limit = 80.0
        return self.value > limit

    def get_formatted_value(self):
        """Возвращает значение с единицей измерения"""
        unit = "cm" if self.sensor.sensor_type == "water_level" else "units"
        return f"{self.value:.2f} {unit}"


User = get_user_model()

class AdminUser(User):
    """
    Класс User(Admin) из UML.
    Реализован как Proxy Model: он использует ту же таблицу auth_user,
    но добавляет специфические методы бизнес-логики.
    """
    class Meta:
        proxy = True
        verbose_name = 'System Administrator'
        verbose_name_plural = 'System Administrators'

    def manage_sensor(self, action: str, data: dict):
        """
        Метод из UML: manage_sensor(action, data)
        Позволяет создавать, обновлять или удалять сенсоры.
        """
        Sensor = apps.get_model('Sensors', 'Sensor')

        if action == 'create':
            return Sensor.objects.create(owner=self, **data)

        elif action == 'update':
            sensor_id = data.pop('id', None)
            if not sensor_id:
                return None
            Sensor.objects.filter(id=sensor_id).update(**data)
            return Sensor.objects.get(id=sensor_id)

        elif action == 'delete':
            sensor_id = data.get('id')
            Sensor.objects.filter(id=sensor_id).delete()
            return None

    @staticmethod
    def configure_analyzer_rules(rules: dict) -> bool:
        """
        Метод из UML: configure_analyzer_rules(rules)
        Обновляет или создает правила анализа.
        rules пример: {'water_level': {'warning': 50, 'critical': 80}}
        """
        AnalysisRule = apps.get_model('analysis', 'AnalysisRule')

        try:
            for sensor_type, thresholds in rules.items():
                AnalysisRule.objects.update_or_create(
                    sensor_type=sensor_type,
                    defaults={
                        'warning_threshold': thresholds['warning'],
                        'critical_threshold': thresholds['critical']
                    }
                )
            return True
        except Exception as e:
            print(f"Error configuring rules: {e}")
            return False

    @staticmethod
    def view_active_alerts():
        """
        Метод из UML: view_active_alerts()
        Возвращает список активных тревог.
        """
        Alert = apps.get_model('analysis', 'Alert')
        return Alert.objects.filter(is_active=True)

    @staticmethod
    def initiate_notifications(alert_id: int) -> int:
        """
        Метод из UML: initiate_notifications(alert)
        Принудительно запускает рассылку уведомлений для конкретной тревоги.
        Возвращает количество созданных уведомлений.
        """
        Alert = apps.get_model('analysis', 'Alert')
        Subscriber = apps.get_model('notifications', 'Subscriber')
        Notification = apps.get_model('notifications', 'Notification')

        try:
            alert = Alert.objects.get(id=alert_id)

            subscribers = Subscriber.objects.filter(region=alert.sensor.region)

            count = 0
            for sub in subscribers:

                notif_type = 'email' if sub.email else 'sms'
                Notification.objects.create(
                    alert=alert,
                    recipient=sub,
                    notification_type=notif_type
                )
                count += 1
            return count
        except Alert.DoesNotExist:
            return 0