# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-20 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0018_auto_20190814_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiz_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]