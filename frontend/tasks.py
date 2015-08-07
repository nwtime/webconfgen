from __future__ import absolute_import

from celery import shared_task
from .models import Upload

from django.core.files.base import ContentFile

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
        upload = Upload.objects.filter(pk=id)[0]
    else:
        return "Called without argument"

    if upload.uploads_status == "AW":
        upload.uploads_input_file_url.save(str(upload.uploads_uuid), ContentFile(upload.uploads_input_string), True)
        return "Saved"
