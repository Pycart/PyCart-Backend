# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import taggit.managers
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150601_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('is_browseable', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('no_punctuation_name', models.CharField(db_index=True, max_length=200, blank=True)),
                ('was_created_on_tsm', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='main.Item_Tag', null=True)),
                ('tag', models.ForeignKey(to='main.Item_Tag')),
            ],
            options={
                'verbose_name': 'Item Tag',
                'verbose_name_plural': 'Item Tags',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='weight',
            field=models.DecimalField(default=1, max_digits=6, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 16, 22, 5, 451357, tzinfo=utc), verbose_name=b'date joined'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(to='main.Item_Tag', through='main.Item_Tag', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
