from django.db import models
from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Photo(models.Model):
    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to='images/')
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['published_at']

    def __str__(self):
        return f'Photo by {self.published_by.username}'




