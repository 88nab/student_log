# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-13 16:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0016_voteforquiz_videoid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voteforquiz',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='voteforquiz',
            name='videoID',
        ),
        migrations.RemoveField(
            model_name='voteforquiz',
            name='voter',
        ),
        migrations.DeleteModel(
            name='VoteForQuiz',
        ),
    ]
