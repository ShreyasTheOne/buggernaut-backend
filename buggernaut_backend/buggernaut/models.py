from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    enrolment_number = models.CharField(max_length=15)
    access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Project(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    wiki = models.CharField(max_length=500)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    deployed = models.BooleanField(default=False)
    created_at = models.DateTimeField('time published', default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


class Issue(models.Model):
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, related_name="issue_assigned_to_user", on_delete=models.CASCADE)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="issue_reported_by_user", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, default="Subject")
    description = models.CharField(max_length=300, default="Description")
    priority = models.PositiveSmallIntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=2)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField('time published', default=datetime.now)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['priority', 'created_at']
