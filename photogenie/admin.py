from django.contrib import admin

from photogenie.models import Category, UserPost


class UserPostAdmin(admin.ModelAdmin):
    list_display = ['published_by', 'published_at', 'views', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u', '.join(o.name for o in obj.tags.all())


admin.site.register(Category)
admin.site.register(UserPost, UserPostAdmin)


