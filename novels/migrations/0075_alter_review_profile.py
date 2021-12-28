# Generated by Django 3.2.8 on 2021-12-21 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_remove_history_username'),
        ('novels', '0074_alter_novel_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_review', to='profiles.profile'),
        ),
    ]
