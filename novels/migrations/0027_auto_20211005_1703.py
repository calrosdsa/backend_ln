# Generated by Django 3.2.5 on 2021-10-05 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0026_auto_20211005_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='novel',
        ),
        migrations.AddField(
            model_name='library',
            name='novel',
            field=models.ManyToManyField(null=True, related_name='library', to='novels.Novel'),
        ),
    ]
