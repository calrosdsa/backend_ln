# Generated by Django 3.2.8 on 2022-01-03 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0091_alter_librarymodel_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarymodel',
            name='option',
            field=models.IntegerField(blank=True, choices=[(2, 'Completed'), (3, 'Favorites')], null=True),
        ),
    ]
