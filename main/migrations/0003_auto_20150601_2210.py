# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('main', '0002_auto_20150601_1754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='shopuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 1, 22, 9, 38, 304590, tzinfo=utc), verbose_name=b'date joined'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='email',
            field=models.EmailField(default=1, unique=True, max_length=255, verbose_name=b'email address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopuser',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name=b'first name', blank=True),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name=b'active'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name=b'staff status'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name=b'last name', blank=True),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
