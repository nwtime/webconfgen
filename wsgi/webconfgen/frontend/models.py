"""
    The DB layer for frontend models.

    Upload class contains the files uploaded by user to full parse.
    Snippet class contains the snippets used for the generation of ntp.conf.
    Version is an abstration for a version.
"""


from textwrap import TextWrapper
from uuid import uuid4

from django.db import models

# Create your models here.

COMMENT_TEXT_WRAPPER = TextWrapper(
    initial_indent='# ',
    subsequent_indent='# ',
    break_long_words=False,
)

UPLOADS_STATUS_CHOICES = (
    ('AW', 'Awaiting Processing'),
    ('PR', 'Processing'),
    ('RE', 'Ready'),
    ('ER', 'Errorred'),
)


class Version(models.Model):
    """
        Contains a list of supported versions, which other classed
        refer to via ManyToManyField
    """
    versions_version = models.CharField(
        max_length=255,
        unique=True,
        help_text="Expected Version format = int.int.int"
    )

    def __unicode__(self):
        """
            Covert to unicode string.
        """
        return u'%s ' % (self.versions_version)

    def convert_to_list(self):
        """
            Converts to a list of split by major and minor version.

            Assumes delimiter to be '.'
        """
        return self.versions_version.split('.')


class Upload(models.Model):
    """
        Contains the files uploaded by user to be fully parsed.
    """
    uploads_owner = models.ForeignKey(
        'auth.user',
        null=True,
    )
    uploads_timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    uploads_input_string = models.TextField()
    uploads_uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid4
    )
    uploads_output_file_url = models.FileField(
        blank=True,
        null=True,
        editable=False,
    )
    uploads_input_file_url = models.FileField(
        blank=True,
        null=True,
        editable=False,
    )
    uploads_version = models.ForeignKey(
        Version
    )
    uploads_status = models.CharField(
        max_length=2,
        choices=UPLOADS_STATUS_CHOICES,
        default='AW',
        editable=False,
    )

    def __unicode__(self):
        """
            Converts to unicode string.
        """
        return "%s - %s - %s" % (self.uploads_uuid, self.uploads_version, self.uploads_status)

    def get_raw(self):
        """
            Returns a raw representation of an upload.
        """
        return u'%s' % (self.uploads_input_string)

    def save(self, *args, **kwargs):
        """
            Overriding save to edit the model when a new object is edited
        """
        if self.uploads_status != 'PR':
            self.uploads_status = 'AW'
        super(Upload, self).save(*args, **kwargs)


class Snippet(models.Model):
    """
        Contains snippets which can be used to generate an ntp.conf
    """
    snippets_name = models.CharField(
        max_length=255,
    )
    snippets_description = models.CharField(
        max_length=255,
        default='',
    )
    snippets_file_text = models.TextField()
    snippets_owner = models.ForeignKey(
        'auth.user',
        null=True,
    )
    snippets_timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    snippets_helper_text = models.TextField()
    snippets_mutually_exclusive = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
    )
    snippets_version = models.ManyToManyField(
        Version,
        symmetrical=False,
    )
    snippets_uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid4
    )

    def __unicode__(self):
        """
            Converts to unicode string.
        """
        return u'%s' % (self.snippets_name)

    def get_raw(self):
        """
            Returns a raw representation of a snippet
        """
        return u'%s\n%s' % (COMMENT_TEXT_WRAPPER.fill(self.snippets_helper_text), self.snippets_file_text)
