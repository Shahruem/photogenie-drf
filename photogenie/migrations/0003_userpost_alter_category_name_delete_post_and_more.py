# Generated by Django 4.2.2 on 2023-08-05 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photogenie', '0002_rename_likes_post_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='images')),
                ('views', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['published_at'],
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='userpost',
            name='categories',
            field=models.ManyToManyField(to='photogenie.category'),
        ),
        migrations.AddField(
            model_name='userpost',
            name='published_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userpost',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
