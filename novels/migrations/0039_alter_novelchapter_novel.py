# Generated by Django 3.2.5 on 2021-10-09 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0038_novelchapter_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novelchapter',
            name='novel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='novel_chapter', to='novels.novel'),
        ),
    ]
