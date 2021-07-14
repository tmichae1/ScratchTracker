from django.db import models
from medication.models import NasalSpray, Ointment
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class DailyReport(models.Model):
    LEFT = 'left'
    RIGHT = 'right'
    BOTH = 'both'
    CHOICES = [(LEFT, 'Left'),
               (RIGHT, 'Right'),
               (BOTH, 'Both')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    ointment_used = models.ForeignKey(Ointment, on_delete=models.CASCADE, null=True, blank=True)
    nasal_spray_used = models.ForeignKey(NasalSpray, on_delete=models.CASCADE, null=True, blank=True)
    nostril_used = models.CharField(max_length=5, choices=CHOICES, null=True, blank=True)
    antihistamine_120mg = models.IntegerField(validators=[MaxValueValidator(9), MinValueValidator(0)], null=True, blank=True)
    steroid_tablet = models.IntegerField(validators=[MaxValueValidator(9), MinValueValidator(0)], null=True, blank=True)
    inhaler = models.IntegerField(validators=[MaxValueValidator(9), MinValueValidator(0)], null=True, blank=True)
    extra_info = models.TextField(max_length=400, null=True, blank=True)
    scalp_steroid = models.BooleanField()

    def __str__(self):
        return "Daily report for {0} {1}: {2}".format(self.user.first_name, self.user.last_name, self.date.strftime("%d/%m/%Y"))



class MedicalReportScores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.FloatField()


class MedicalReportDailyScores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.FloatField()

    def __str__(self):
        return "{0} {1} - {2} - {3}".format(self.user.first_name, self.user.last_name, self.score, self.date.strftime("%d/%m/%Y"))

