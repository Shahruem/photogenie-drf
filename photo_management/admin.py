from django.contrib import admin
from photo_management.models import Category, Photo


admin.site.register([Category, Photo])


