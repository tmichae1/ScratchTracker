from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Scratch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return "{0}, {1} {2}, {3}, {4}".format(self.user, self.user.first_name, self.user.last_name, self.date.strftime("%d/%m/%Y"), self.time.strftime("%H:%M:%S"))


class DailyScratchCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return "{0} total scratches on {1} for {2} {3}".format(self.total, self.date.strftime("%d/%m/%Y"), self.user.first_name, self.user.last_name)

class ScratchMonthlyAvg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total = models.IntegerField()

class NightScratch(models.Model):
    BEFORE_12 = "before 12am"
    AFTER_12_BEFORE_1 = "between 12am and 1am"
    AFTER_1_BEFORE_2 = "between 1am and 2am"
    AFTER_2 = "after 2am"
    CHOICES = [(BEFORE_12, 'Before 12am'),
               (AFTER_12_BEFORE_1, 'Between 12am and 1am'),
               (AFTER_1_BEFORE_2, 'Between 1am and 2am'),
               (AFTER_2, 'After 2am')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_of_10th_scratch = models.CharField(choices=CHOICES, max_length=22)
    points = models.IntegerField()

    def __str__(self):
        return "{0} {1} got {2} points on {3}".format(self.user.first_name, self.user.last_name, self.points, self.date)

class NightScratchMonthlyAvg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    points = models.FloatField()