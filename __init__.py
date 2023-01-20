from django.template.defaultfilters import register
from .filters import valid_xml_element

register.filter('valid_xml_element', valid_xml_element)

__version__ = '0.1.0-dev1'
