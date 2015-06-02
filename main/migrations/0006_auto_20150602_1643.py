# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150602_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop_item_tag',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='shop_item_tag',
            name='no_punctuation_name',
        ),
        migrations.RemoveField(
            model_name='shop_item_tag',
            name='was_created_on_tsm',
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 16, 43, 47, 376043, tzinfo=utc), verbose_name=b'date joined'),
        ),
    ]
