# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 16:16
from __future__ import unicode_literals

import django.db.models.deletion
import djgeojson.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    replaces = [('mainapp', '0001_squashed_0055_file_mentioned_persons'), ('mainapp', '0002_auto_20171222_1521')]

    operations = [
        migrations.CreateModel(
            name='AgendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('key', models.CharField(blank=True, max_length=20, null=True)),
                ('title', models.TextField()),
                ('position', models.IntegerField()),
                ('public', models.NullBooleanField()),
                ('result', models.CharField(blank=True, max_length=200, null=True)),
                ('resolution_text', models.TextField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['meeting', 'position'],
            },
        ),
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField()),
                ('short_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('authoritative', models.NullBooleanField()),
                ('role', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('storage_filename', models.CharField(max_length=200)),
                ('displayed_filename', models.CharField(max_length=200)),
                ('mime_type', models.CharField(max_length=255)),
                ('legal_date', models.DateField(blank=True, null=True)),
                ('filesize', models.IntegerField()),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('parsed_text', models.TextField(blank=True, null=True)),
                ('license', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LegislativeTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField()),
                ('short_name', models.CharField(max_length=50)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField()),
                ('short_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_official', models.BooleanField()),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('geometry', djgeojson.fields.GeometryField(default=None)),
                ('bodies', models.ManyToManyField(blank=True, to='mainapp.Body')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField()),
                ('short_name', models.CharField(max_length=50)),
                ('cancelled', models.BooleanField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('public', models.IntegerField(blank=True, choices=[(0, 'unknown'), (1, 'public'), (2, 'not public'),
                                                                    (3, 'splitted')], default=0)),
                ('auxiliary_files',
                 models.ManyToManyField(blank=True, related_name='meeting_auxiliary_files', to='mainapp.File')),
                ('invitation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='meeting_invitation', to='mainapp.File')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='mainapp.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField()),
                ('short_name', models.CharField(max_length=50)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('color', models.CharField(blank=True, max_length=6, null=True)),
                ('logo', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Body')),
                ('legislative_terms', models.ManyToManyField(blank=True, to='mainapp.LegislativeTerm')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='mainapp.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('role', models.CharField(blank=True, max_length=200, null=True)),
                ('organization',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField()),
                ('short_name', models.CharField(max_length=50)),
                ('reference_number', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('legal_date', models.DateField(blank=True, null=True)),
                ('change_request_of',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='mainapp.Paper')),
                ('files', models.ManyToManyField(blank=True, to='mainapp.File')),
                ('main_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                related_name='paper_main_file', to='mainapp.File')),
                ('organizations', models.ManyToManyField(blank=True, to='mainapp.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaperType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_type', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('given_name', models.CharField(max_length=50)),
                ('family_name', models.CharField(max_length=50)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='mainapp.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchPoi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('displayed_name', models.CharField(max_length=1000)),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('osm_amenity', models.CharField(max_length=1000, null=True)),
                ('geometry', djgeojson.fields.GeometryField(null=True)),
                ('exclude_from_search', models.BooleanField(default=False)),
                ('bodies', models.ManyToManyField(blank=True, to='mainapp.Body')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchStreet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oparl_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('displayed_name', models.CharField(max_length=1000)),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('exclude_from_search', models.BooleanField(default=False)),
                ('bodies', models.ManyToManyField(blank=True, to='mainapp.Body')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_string', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_match', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user',
                 models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile',
                                      to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.AddField(
            model_name='paper',
            name='paper_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='mainapp.PaperType'),
        ),
        migrations.AddField(
            model_name='paper',
            name='persons',
            field=models.ManyToManyField(blank=True, to='mainapp.Person'),
        ),
        migrations.AddField(
            model_name='organizationmembership',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Person'),
        ),
        migrations.AddField(
            model_name='organization',
            name='organization_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.OrganizationType'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='organizations',
            field=models.ManyToManyField(blank=True, to='mainapp.Organization'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='persons',
            field=models.ManyToManyField(blank=True, to='mainapp.Person'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='results_protocol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='meeting_results_protocol', to='mainapp.File'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='verbatim_protocol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='meeting_verbatim_protocol', to='mainapp.File'),
        ),
        migrations.AddField(
            model_name='file',
            name='locations',
            field=models.ManyToManyField(blank=True, to='mainapp.Location'),
        ),
        migrations.AddField(
            model_name='file',
            name='mentioned_persons',
            field=models.ManyToManyField(blank=True, to='mainapp.Person'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='meeting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='mainapp.Meeting'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='organizations',
            field=models.ManyToManyField(blank=True, to='mainapp.Organization'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='paper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='mainapp.Paper'),
        ),
        migrations.AddField(
            model_name='body',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='body_center', to='mainapp.Location'),
        ),
        migrations.AddField(
            model_name='body',
            name='legislative_terms',
            field=models.ManyToManyField(blank=True, to='mainapp.LegislativeTerm'),
        ),
        migrations.AddField(
            model_name='body',
            name='outline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='body_outline', to='mainapp.Location'),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='auxiliary_file',
            field=models.ManyToManyField(blank=True, related_name='auxiliary_file', to='mainapp.File'),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='consultation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='mainapp.Consultation'),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Meeting'),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='resolution_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='resolution_file', to='mainapp.File'),
        ),
    ]
