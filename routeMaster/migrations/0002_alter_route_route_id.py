# Generated by Django 5.2 on 2025-07-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routeMaster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='route_id',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
