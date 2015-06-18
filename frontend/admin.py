from django.contrib import admin
from .models import Snippet, Upload, Version

# Register your models here.
admin.site.register(Snippet)
admin.site.register(Upload)
admin.site.register(Version)
