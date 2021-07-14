from django.db import models

# Create your models here.


class Ointment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class NasalSpray(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


