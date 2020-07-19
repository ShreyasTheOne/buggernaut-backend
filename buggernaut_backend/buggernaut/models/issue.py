from django.db import models
from datetime import datetime
from django.conf import settings
from buggernaut.models import Project, Tag
from tinymce.models import HTMLField


# Create your models here.


class Issue(models.Model):
    priority = models.PositiveSmallIntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=2)
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    created_at = models.DateTimeField('time published', default=datetime.now)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    subject = models.CharField(max_length=100, default="Subject")
    resolved = models.BooleanField(default=False)
    editorID = models.CharField(max_length=1000)
    description = HTMLField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="issue_assigned_to_user",
                                    on_delete=models.CASCADE,
                                    default=None,
                                    null=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="issue_resolved_by_user",
                                    on_delete=models.CASCADE,
                                    default=None,
                                    null=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="issue_reported_by_user",
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

    def __repr__(self):
        return self.subject

    class Meta:
        ordering = ['-created_at', 'priority']
