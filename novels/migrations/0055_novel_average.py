# Generated by Django 3.2.5 on 2021-10-16 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0054_novel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='average',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
