# Generated by Django 3.2.5 on 2021-10-15 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0050_remove_novel_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='slug',
            field=models.SlugField(default='', max_length=64),
        ),
    ]
