# Generated by Django 3.2.8 on 2021-12-10 01:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0007_alter_novelnotifiactions_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novelnotifiactions',
            name='user',
        ),
        migrations.AddField(
            model_name='novelnotifiactions',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
