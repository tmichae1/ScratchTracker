from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.DailyReport)
admin.site.register(models.MedicalReportScores)
admin.site.register(models.MedicalReportDailyScores)