# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_snippet_snippets_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='uploads_input_file_url',
            field=models.FileField(upload_to=b'', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='upload',
            name='uploads_output_file_url',
            field=models.FileField(upload_to=b'', null=True, editable=False, blank=True),
        ),
    ]
