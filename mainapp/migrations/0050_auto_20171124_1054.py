# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0049_auto_20171118_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='organization',
            new_name='organizations',
        ),
    ]
