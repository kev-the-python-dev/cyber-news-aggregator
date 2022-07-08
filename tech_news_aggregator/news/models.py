from django.db import models

class Headline(models.Model):
    title = models.CharField(max_length=120)
    image = models.URLField(null=True, blank=True, max_length=400)
    date = models.TextField(null=True, max_length=50)
    url = models.TextField(max_length=200)

    def __str__(self):
        return self.title

    # Ensure 
    class Meta:
        unique_together = ['title', 'image', 'date','url']
