from django.test import TestCase
from .models import Upload, Snippet, Version

# Create your tests here.


class SanityCheck(TestCase):
    def test_object_creation(self):
        version = Version(versions_version="0.0.0")
        upload = Upload()
        snippet = Snippet()
        
