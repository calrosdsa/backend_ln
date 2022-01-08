# Generated by Django 3.2.8 on 2022-01-06 20:34

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0100_alter_librarymodel_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarymodel',
            name='option',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)]), blank=True, null=True, size=None),
        ),
    ]
