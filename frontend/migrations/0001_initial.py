# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('snippets_name', models.CharField(max_length=255)),
                ('snippets_description', models.CharField(default=b'', max_length=255)),
                ('snippets_file_text', models.TextField()),
                ('snippets_timestamp', models.DateTimeField(auto_now_add=True)),
                ('snippets_helper_text', models.TextField()),
                ('snippets_mutually_exclusive', models.ManyToManyField(related_name='snippets_mutually_exclusive_rel_+', to='frontend.Snippet', blank=True)),
                ('snippets_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uploads_timestamp', models.DateTimeField(auto_now_add=True)),
                ('uploads_input_string', models.TextField()),
                ('uploads_uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('uploads_output_file_url', models.URLField(null=True, editable=False, blank=True)),
                ('uploads_input_file_url', models.URLField(null=True, editable=False, blank=True)),
                ('uploads_status', models.CharField(default=b'AW', max_length=2, editable=False, choices=[(b'AW', b'Awaiting Processing'), (b'PR', b'Processing'), (b'RE', b'Ready'), (b'ER', b'Errorred')])),
                ('uploads_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('versions_version', models.CharField(help_text=b'Expected Version format = int.int.int', unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='upload',
            name='uploads_version',
            field=models.ForeignKey(to='frontend.Version'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='snippets_version',
            field=models.ManyToManyField(to='frontend.Version'),
        ),
    ]
