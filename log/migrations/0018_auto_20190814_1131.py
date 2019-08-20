# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-14 11:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0017_auto_20190813_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=500)),
                ('first_answer', models.CharField(max_length=250)),
                ('second_answer', models.CharField(max_length=250)),
                ('third_answer', models.CharField(max_length=250)),
                ('fourth_answer', models.CharField(max_length=250)),
                ('correct_answer', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quizID', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'Student'), ('LECTURER', 'Lecturer')], default='STUDENT', max_length=8),
        ),
        migrations.AddField(
            model_name='quiz',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log.Subject'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log.Video'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log.Quiz'),
        ),
    ]
