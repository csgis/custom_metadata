from django import template
from re import sub
from django.utils.text import slugify

register = template.Library()

@register.filter
def valid_xml_element(value):
    value = slugify(value)
    value = value.replace("-", "_")
    if not value[0].isalpha():
        value = '_' + value
    return value
