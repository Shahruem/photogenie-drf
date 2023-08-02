from django.db import models
from taggit.managers import TaggableManager

from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Post(models.Model):
    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    categories = models.ManyToManyField(Category)
    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['published_at']

    def __str__(self):
        return f'Photo by {self.published_by.username}'




