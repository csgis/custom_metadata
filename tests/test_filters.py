from django.test import TestCase
from custom_metadata.filters import valid_xml_element
from unittest import mock, TestCase

# run with
# DATABASE_URL=postgis://geonode:geonode@localhost:5432/geonode
# DJANGO_SETTINGS_MODULE=geonode.settings pytest -p no:warnings custom_metadata/tests

# Todo: Add and improve tests

class FilterTests(TestCase):
    @mock.patch("django.db.utils.ConnectionHandler.__getitem__")
    def test_valid_xml_element(self, mock_getitem):
        self.assertEqual(valid_xml_element("D o$$<s@"), "d_os")
        self.assertEqual(valid_xml_element("Schönbuchner"), "schonbuchner")
