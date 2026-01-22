# apps/reports/services.py

import csv
import json # Добавили
from datetime import timedelta # Добавили
from django.apps import apps
from django.http import HttpResponse
from django.db.models import Count # Добавили
from django.db.models.functions import TruncDate # Добавили

class ReportService:
    """
    Реализация класса Report из UML.
    """

    @staticmethod
    def get_daily_stats(start_date, end_date):
        """
        Считает количество тревог по дням для построения общего графика.
        """
        Alert = apps.get_model('analysis', 'Alert')


        stats_query = Alert.objects.filter(
            created_at__range=(start_date, end_date)
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')


        stats_dict = {item['date']: item['count'] for item in stats_query}


        labels = []
        data = []
        current_date = start_date.date()
        end_date_date = end_date.date()

        while current_date <= end_date_date:
            labels.append(current_date.strftime("%d.%m"))
            data.append(stats_dict.get(current_date, 0))
            current_date += timedelta(days=1)

        return {
            'labels': labels,
            'data': data
        }


    @staticmethod
    def get_alert_summary(start_date, end_date):
        Alert = apps.get_model('analysis', 'Alert')
        alerts = Alert.objects.filter(created_at__range=(start_date, end_date))

        return {
            'total_alerts': alerts.count(),
            'critical_count': alerts.filter(level='critical').count(),
            'warning_count': alerts.filter(level='warning').count(),
        }