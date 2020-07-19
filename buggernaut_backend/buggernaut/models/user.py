from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    enrolment_number = models.CharField(max_length=15)
    display_picture = models.CharField(max_length=500)
    full_name = models.CharField(max_length=50)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return self.first_name + " " + self.last_name
