# Generated by Django 3.2.5 on 2021-09-26 03:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('novels', '0008_reply_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply_review',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='reply_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
