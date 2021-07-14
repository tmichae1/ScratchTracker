from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Scratch)
admin.site.register(models.DailyScratchCount)
admin.site.register(models.NightScratch)
admin.site.register(models.NightScratchMonthlyAvg)
admin.site.register(models.ScratchMonthlyAvg)