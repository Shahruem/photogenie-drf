from django.contrib import admin

from photogenie.models import Category, UserPost


class UserPostAdmin(admin.ModelAdmin):
    """ Handles admin panel for UserPost model. """

    list_display = ['published_by', 'published_at', 'views', 'tag_list']

    def get_queryset(self, request):
        """ Returns query optimised list of tags for the requested user. """

        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        """ Returns comma seperated tags from the tag list. """
        return u', '.join(o.name for o in obj.tags.all())


admin.site.register(Category)
admin.site.register(UserPost, UserPostAdmin)


