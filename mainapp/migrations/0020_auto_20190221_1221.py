# Generated by Django 2.1.7 on 2019-02-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20181227_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaper',
            name='change_request_of',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='mainapp.Paper'),
        ),
    ]
