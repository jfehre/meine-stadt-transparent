# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-16 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0007_auto_20180208_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='oparl_access_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='oparl_download_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalfile',
            name='oparl_access_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalfile',
            name='oparl_download_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
