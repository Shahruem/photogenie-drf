from django.db import models
from taggit.managers import TaggableManager

from authentication.models import User
from photogenie.constants import IMAGE_PATH


class Category(models.Model):
    """ Model for Category of Posts. """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class UserPost(models.Model):
    """ Model for posts uploaded by users. """

    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to=IMAGE_PATH)
    categories = models.ManyToManyField(Category)
    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['published_at']

    def __str__(self):
        return f'Photo by {self.published_by.username}'

    @property
    def dimensions(self):
        """ Returns the 'x' seperated height and width of image of the Post instance as dimensions. """

        return f'{self.image.height}x{self.image.width}'
