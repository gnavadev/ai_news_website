from django.db import models

class NewsPost(models.Model):
    headline = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline
