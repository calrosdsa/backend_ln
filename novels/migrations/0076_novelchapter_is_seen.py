# Generated by Django 3.2.8 on 2021-12-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0075_alter_review_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='novelchapter',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
