"""
The celery instance of the project webconfgen.

Contains the setup settings for celery to work with
django.
"""


from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webconfgen.settings')

app = Celery('webconfgen')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """
        A function used for internal debugging.
    """
    print 'Request: {0!r}'.format(self.request)
