from __future__ import absolute_import

from celery import shared_task
from .models import Upload

from webconfgen.celery import app
import logging
logger = logging.getLogger(__name__)


@shared_task
def test(param):
    """
        A tester method used for internal debugging
    """
    return 'The test task executed with argument "%s" ' % param


@app.task()
def parser_enqueue(id):
    """
        This function is called with a valid id of an Upload object.
    """
    if id:
        item = Upload.objects.filter(pk=id)[0]
        item.uploads_status = 'PR'
        item.save()
    else:
        return "Called without argument"
