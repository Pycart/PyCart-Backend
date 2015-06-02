# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150602_1705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Item', 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name': 'Option', 'verbose_name_plural': 'Options'},
        ),
        migrations.AlterModelOptions(
            name='shop_tagged_item',
            options={'verbose_name': 'Tagged Item', 'verbose_name_plural': 'Tagged Items'},
        ),
        migrations.AddField(
            model_name='item',
            name='option',
            field=models.ForeignKey(default=1, to='main.Option'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop_item_tag',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='main.Shop_Item_Tag', null=True),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 17, 48, 1, 961942, tzinfo=utc), verbose_name=b'date joined'),
        ),
    ]
