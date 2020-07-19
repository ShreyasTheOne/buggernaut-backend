from django.db import models


class Image(models.Model):
    editorID = models.CharField(max_length=1000)
    url = models.ImageField(upload_to='rtfImages/', blank=False, null=False)

    def __str__(self):
        return self.url.url