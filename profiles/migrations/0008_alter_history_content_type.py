# Generated by Django 3.2.8 on 2021-10-21 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0007_alter_history_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
    ]
