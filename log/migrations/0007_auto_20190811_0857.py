# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-11 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0006_auto_20190811_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentvideolinkuploads',
            name='upload_link_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
