# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import datetime
from django.utils.timezone import utc
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0004_auto_20150602_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop_Item_Tag',
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
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='main.Shop_Item_Tag', null=True)),
            ],
            options={
                'verbose_name': 'Item Tag',
                'verbose_name_plural': 'Item Tags',
            },
        ),
        migrations.CreateModel(
            name='Shop_Tagged_Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('start_date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('end_date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('content_type', models.ForeignKey(related_name='main_shop_tagged_item_tagged_items', verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(to='main.Shop_Item_Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='item_tag',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='item_tag',
            name='tag',
        ),
        migrations.AddField(
            model_name='item',
            name='option',
            field=models.ForeignKey(default=1, to='main.Option'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(to='main.Shop_Item_Tag', through='main.Shop_Tagged_Item', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 16, 41, 33, 825459, tzinfo=utc), verbose_name=b'date joined'),
        ),
        migrations.DeleteModel(
            name='Item_Tag',
        ),
    ]
