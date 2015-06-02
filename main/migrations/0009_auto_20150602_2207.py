# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20150602_1748'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AlterField(
            model_name='shop_item_tag',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='main.Shop_Item_Tag', null=True),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 22, 7, 38, 768544, tzinfo=utc), verbose_name=b'date joined'),
        ),
    ]
