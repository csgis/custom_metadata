from django.template.defaultfilters import register
from .filters import valid_xml_element

register.filter('valid_xml_element', valid_xml_element)

__author__ = "Toni Schönbuchner | CSGIS"
__copyright__ = "Copyright (C) 2023, Toni Schönbuchner | CSGIS"
__license__ = "GNU General Public License"
__version__ = "0.1.1-dev1"
