from __future__ import absolute_import

from celery import shared_task
from .models import Upload

from webconfgen.celery import app
import logging
logger = logging.getLogger(__name__)


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@app.task()
def parser_enqueue(param):
    id = param.get('id', None)
    if id:
        item = Upload.objects.filter(pk=id)[0]
        item.uploads_status = 'PR'
        item.save()
    else:
        return "Failed"
