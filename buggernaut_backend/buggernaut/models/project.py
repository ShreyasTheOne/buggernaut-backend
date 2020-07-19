from django.db import models
from datetime import datetime
from django.conf import settings
from tinymce.models import HTMLField


class Project(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    image = models.ImageField(upload_to='projectImages/', default='assets/img.png')
    editorID = models.CharField(max_length=1000)
    wiki = HTMLField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    deployed = models.BooleanField(default=False)
    created_at = models.DateTimeField('time published', default=datetime.now)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
