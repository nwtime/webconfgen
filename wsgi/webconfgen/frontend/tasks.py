"""
The celery task queue functions for the
webconfgen project.
"""


from __future__ import absolute_import

import logging

from celery import shared_task
from django.core.files.base import ContentFile

from backend.parser import Parser
from webconfgen.celery import app

from .models import Upload

logger = logging.getLogger(__name__)


@shared_task
def test(param):
    """
        A tester method used for internal debugging
    """
    return 'The test task executed with argument "%s" ' % param


@app.task(bind=True)
def parser_enqueue(self, database_key):
    """
        This function is called with a valid id of an Upload object.
        This handles the parsing for the upload objects that come in.

        This function assumes that the upload object is not deleted
        until the task processing is complete.

        A task with uploads_status = "PR" is silently failed.
    """
    if database_key:
        upload = Upload.objects.filter(pk=database_key)[0]
    else:
        return "Called without argument"

    if upload.uploads_status == "PR":
        return "Sliently failing because existing task processing is not complete : " + str(upload)

    upload.uploads_input_file_url.save(str(upload.uploads_uuid) + ".in.conf", ContentFile(upload.uploads_input_string), True)
    upload.uploads_status = "PR"
    upload.save()

    try:
        parser = Parser(upload.uploads_input_file_url.file.file)
        output = parser.parse()
        upload.uploads_output_file_url.save(str(upload.uploads_uuid) + ".out.conf", ContentFile(output), True)
        upload.uploads_status = "RE"
        upload.save()
    except Exception as e:
        upload.uploads_status = "ER"
        upload.save()
        return "Failed : " + str(e)

    return "Sucessfully parsed " + str(upload)
