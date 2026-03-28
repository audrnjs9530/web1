from django.db import models
from django.conf import settings
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
    )

    @property
    def points(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.id}, {self.title}, {self.author}"

    def __str__(self):
        return f"{self.id}, {self.title}, {self.author}"