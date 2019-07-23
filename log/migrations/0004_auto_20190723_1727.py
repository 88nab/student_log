# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-23 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_auto_20190722_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_email',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='lecturer_email',
        ),
        migrations.RemoveField(
            model_name='video',
            name='id',
        ),
        migrations.AddField(
            model_name='video',
            name='videoDescription',
            field=models.CharField(default='xxx', max_length=250),
        ),
        migrations.AddField(
            model_name='video',
            name='videoFile',
            field=models.FileField(null=True, upload_to='videos/', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='video',
            name='videoID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]