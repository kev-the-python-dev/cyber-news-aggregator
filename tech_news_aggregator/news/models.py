from django.db import models

class Headline(models.Model):
    title = models.CharField(max_length=120)
    image = models.URLField(null=True, blank=True)
    url = models.TextField()

    def __str__(self):
        return self.title
