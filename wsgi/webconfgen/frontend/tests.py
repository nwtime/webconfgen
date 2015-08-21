"""
Django unit tests for webconfgen
"""


from django.test import TestCase

from .models import Snippet, Upload, Version


class SanityCheckTest(TestCase):
    """
        A series of sanity checks.
    """
    def test_object_creation(self):
        """
            Tests for sane creation of objectss
        """
        test_input = '''
            This is a test string for parsing
        '''
        test_description = 'This is a test description.'
        test_helper_text = 'This is a test helper test.'
        test_file_text = 'This is a file text test'
        test_version = '0.0.0'
        version = Version.objects.create(
            versions_version=test_version
        )
        self.assertNotEqual(Version.objects.all(), [])
        self.assertEqual(version.versions_version, test_version)
        upload = Upload.objects.create(
            uploads_version=version,
            uploads_input_string=test_input
        )
        self.assertNotEqual(Upload.objects.all(), [])
        self.assertEqual(upload.uploads_input_string, test_input)
        self.assertEqual(upload.uploads_version, version)
        self.assertTrue(upload.uploads_uuid)
        self.assertTrue(upload.uploads_timestamp)
        self.assertEqual(upload.uploads_status, 'AW')
        snippet = Snippet.objects.create(
            snippets_description=test_description,
            snippets_helper_text=test_helper_text,
            snippets_file_text=test_file_text,
        )
        snippet.snippets_version.add(version)
        snippet.save()
        self.assertNotEqual(Snippet.objects.all(), [])
        self.assertIn(version, snippet.snippets_version.all())
        self.assertEqual(snippet.snippets_description, test_description)
        self.assertEqual(snippet.snippets_helper_text, test_helper_text)
        self.assertEqual(snippet.snippets_file_text, test_file_text)
        self.assertTrue(snippet.snippets_uuid)
        self.assertTrue(snippet.snippets_timestamp)
