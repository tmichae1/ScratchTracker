from django.urls import path
from . import views

urlpatterns = [
    path('add-daily-report/', views.add_daily_report, name='add-daily-report'),
    path('get-todays-report/', views.get_todays_report, name='get-todays-report'),
    path('all-reports/', views.get_all_reports, name='view-all-reports'),
    path('get-report/<date>/', views.get_report, name='get-report'),
    path('daily-report-exists/', views.daily_report_exists, name='daily-report-exists'),
    path('update-report/<date>/', views.update_medical_report, name='update-report'),
    path('stats-table/', views.view_stats_table, name='stats-table'),
    path('scratch-chart/', views.scratch_score_chart, name='stats-chart')
]