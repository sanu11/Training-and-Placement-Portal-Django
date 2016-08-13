# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-11 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=40)),
                ('criteria', models.FloatField()),
                ('salary', models.IntegerField()),
                ('reg_start_date', models.DateTimeField()),
                ('reg_end_date', models.DateTimeField()),
                ('ppt_date', models.DateTimeField()),
                ('apti_date', models.DateTimeField()),
                ('interview_date', models.DateTimeField()),
                ('last_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('password', models.CharField(max_length=12)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=200)),
                ('branch', models.IntegerField(default=0)),
                ('average', models.FloatField()),
                ('placed', models.IntegerField(default=0)),
                ('active_back', models.IntegerField(default=0)),
                ('num_back', models.IntegerField(default=0)),
                ('company_id', models.IntegerField(default=-1)),
            ],
        ),
    ]
