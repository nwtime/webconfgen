# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20150806_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='snippets_owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='upload',
            name='uploads_owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
