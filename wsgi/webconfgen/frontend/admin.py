"""
Django Admin module.

Registered Snippet Upload and Version to be accessable
via admin access.
"""

from django.contrib import admin

from .models import Snippet, Upload, Version

admin.site.register(Snippet)
admin.site.register(Upload)
admin.site.register(Version)
