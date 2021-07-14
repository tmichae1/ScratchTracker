from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    profile_id = models.CharField(max_length=25)
    full_name = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.full_name, self.user.username)
