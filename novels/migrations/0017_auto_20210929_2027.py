# Generated by Django 3.2.5 on 2021-09-30 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0016_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='novel',
        ),
        migrations.AddField(
            model_name='review',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='categories', to='novels.Category'),
        ),
    ]
