from __future__ import absolute_import

from celery import shared_task
from .models import Upload

from django.core.files.base import ContentFile

from webconfgen.celery import app

from backend.parser import Parser
import logging
logger = logging.getLogger(__name__)


@shared_task
def test(param):
    """
        A tester method used for internal debugging
    """
    return 'The test task executed with argument "%s" ' % param


@app.task(bind=True)
def parser_enqueue(self, id):
    """
        This function is called with a valid id of an Upload object.
    """
    if id:
        upload = Upload.objects.filter(pk=id)[0]
    else:
        return "Called without argument"

    if upload.uploads_status == "PR":
        return "Sliently failing because existing task processing is not complete : " + str(upload)

    upload.uploads_input_file_url.save(str(upload.uploads_uuid) + ".in.conf", ContentFile(upload.uploads_input_string), True)
    upload.uploads_status = "PR"
    upload.save()

    try:
        parser = Parser(upload.uploads_input_file_url)
        output = parser.parse()
        upload.uploads_output_file_url.save(str(upload.uploads_uuid) + ".out.conf", ContentFile(output), True)
        upload.uploads_status = "RE"
        upload.save()
    except Exception as e:
        upload.uploads_status = "ER"
        upload.save()
        return "Failed : " + str(e)

    return "Sucessfully parsed " + str(upload)
