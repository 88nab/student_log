# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-12 15:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0012_filecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filecomment',
            name='reply',
        ),
    ]