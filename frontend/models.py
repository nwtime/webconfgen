"""
    The DB layer for frontend models.

    Uploads class contains the flies uploaded by user to full parse.
"""


from django.db import models
import uuid

# Create your models here.

UPLOADS_STATUS_CHOICES = (
    ('AW', 'Awaiting Processing'),
    ('PR', 'Processing'),
    ('RE', 'Ready'),
    ('ER', 'Errorred'),
)

SNIPPET_TYPE_CHOICES = (
    ('OS', 'Operating System'),
    ('ST', 'Statistics'),
    ('AU', 'Authentication'),
    ('MI', 'Miscellaneous'),
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
        return u'%s ' % (self.versions_version)

    def convert_to_list(self):
        return self.versions_version.split('.')


class Upload(models.Model):
    """
        Contains the files uploaded by user to be fully parsed.
    """
    uploads_owner = models.ForeignKey(
        'auth.user',
    )
    uploads_timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    uploads_input_string = models.TextField()
    uploads_uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    uploads_output_file_uri = models.URLField(
        blank=True,
        null=True,
        editable=False,
    )
    uploads_output_file = models.FileField(
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
        return "%s - %s - %s" % (self.uploads_owner, self.uploads_uuid, self.uploads_version)


class Snippet(models.Model):

    def __unicode__(self):
        return u'%s' % (self.snippets_name)

    snippets_name = models.CharField(
        max_length=255,
    )
    snippets_file_text = models.TextField()
    snippets_owner = models.ForeignKey(
        'auth.user',
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
    snippets_type = models.CharField(
        max_length=2,
        choices=SNIPPET_TYPE_CHOICES,
        default='MI',
    )
