# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150602_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='option',
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 17, 5, 53, 606363, tzinfo=utc), verbose_name=b'date joined'),
        ),
    ]
