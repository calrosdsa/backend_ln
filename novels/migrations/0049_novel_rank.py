# Generated by Django 3.2.5 on 2021-10-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0048_auto_20211014_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
