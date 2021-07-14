from django.urls import path
from . import views
urlpatterns = [
    path('get-stats/', views.get_stats, name='get-stats'),
    path('get-medical-intake-history/', views.get_medical_history_days, name='get-medical-intake-days'),
    path('get-daily-scratch-count/<date>/', views.get_daily_scratch_counts, name='get-daily-scratch-count'),
    path('get-daily-medical-score/<date>/', views.get_daily_medical_scores, name='get-daily-medical-scores'),
    path('get-night-scratch-score/<date>/', views.get_night_scratch_scores, name='get-night-scratch-score')
]
