# Generated by Django 3.2.8 on 2021-12-19 12:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0073_alter_novel_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='average',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=2, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
