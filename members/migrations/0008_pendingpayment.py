# Generated by Django 3.2.20 on 2023-07-08 15:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0007_alter_contactinfo_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('date', models.DateField()),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.paymentmethod')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
    ]
