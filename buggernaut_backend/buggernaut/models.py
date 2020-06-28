from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    enrolment_number = models.CharField(max_length=15)
    display_picture = models.CharField(max_length=500)
    full_name = models.CharField(max_length=50)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return self.first_name + " " + self.last_name


class Project(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    image = models.ImageField(upload_to='projectImages/', default='projectImages/img.png')
    wiki = models.TextField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    deployed = models.BooleanField(default=False)
    created_at = models.DateTimeField('time published', default=datetime.now)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Issue(models.Model):
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="issue_assigned_to_user", on_delete=models.CASCADE, default=None, null=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="issue_resolved_by_user", on_delete=models.CASCADE, default=None, null=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="issue_reported_by_user", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, default="Subject")
    description = models.TextField(default="Description")
    priority = models.PositiveSmallIntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=2)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField('time published', default=datetime.now)

    def __str__(self):
        return self.subject

    def __repr__(self):
        return self.subject

    class Meta:
        ordering = ['-created_at', 'priority']

class Comment(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, related_name="comment_parent", on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, related_name="comment", on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, related_name="commented_by_user", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField('time published', auto_now_add=True)

    class Meta:
        ordering = ['created_at', ]


class Image(models.Model):
    url = models.ImageField(upload_to='rtfImages/', blank=False, null=False)

    def __str__(self):
        return self.url.name
