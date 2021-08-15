# Generated by Django 3.1.3 on 2020-12-06 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0028_auto_20200609_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendaitem',
            name='public',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='authoritative',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalagendaitem',
            name='public',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalconsultation',
            name='authoritative',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
