# apps/reports/views.py

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test
import json

from .services import ReportService

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user)
def analytics_view(request):

    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)


    summary = ReportService.get_alert_summary(start_date, end_date)


    chart_stats = ReportService.get_daily_stats(start_date, end_date)

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'summary': summary,

        'chart_labels_json': json.dumps(chart_stats['labels']),
        'chart_data_json': json.dumps(chart_stats['data']),
    }
    return render(request, 'analytics.html', context)