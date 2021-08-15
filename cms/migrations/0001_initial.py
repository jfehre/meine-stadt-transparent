# Generated by Django 2.1.7 on 2019-02-21 14:04

import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('page_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'A page with a title and some content',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GlossaryEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('key', models.CharField(max_length=512)),
                ('value', wagtail.core.fields.RichTextField()),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlossaryPage',
            fields=[
                ('page_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'A glossary',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('page_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'The landing page for the cms section',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='glossaryentry',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries',
                                                  to='cms.GlossaryPage'),
        ),
    ]
