# Generated by Django 3.2.5 on 2021-10-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0037_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='novelchapter',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
