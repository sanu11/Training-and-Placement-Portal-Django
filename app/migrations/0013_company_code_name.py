# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-20 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_company_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='code_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]