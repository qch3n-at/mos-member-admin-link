# Generated by Django 3.2.20 on 2023-07-09 20:16

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_bankimportmatcher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankimportmatcher',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
