from django.db import models
from django.conf import settings
from buggernaut.models import Issue


class Comment(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, related_name="comment_parent", on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, related_name="comment", on_delete=models.CASCADE)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="commented_by_user", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField('time published', auto_now_add=True)

    class Meta:
        ordering = ['created_at', ]
