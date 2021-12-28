# Generated by Django 3.2.5 on 2021-09-30 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0017_auto_20210929_2027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='novel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='novels.novel'),
        ),
    ]
