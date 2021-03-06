# Generated by Django 3.2.8 on 2022-01-03 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('novels', '0088_auto_20220103_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='novels', through='novels.LibraryModel', to='novels.Novel'),
        ),
        migrations.AlterField(
            model_name='library',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites_novels', to=settings.AUTH_USER_MODEL),
        ),
    ]
