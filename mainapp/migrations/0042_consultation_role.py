# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0041_auto_20171117_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='role',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
