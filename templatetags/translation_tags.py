from django import template
import os
from django.utils.safestring import mark_safe
from django.conf import settings
import json

register = template.Library()

@register.simple_tag
def get_custom_metadata_translations():

    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'metadata_fields',
        'translations.json'
    )

    if hasattr(settings, 'CUSTOM_METADATA_CONFIG_DIR'):
        file_path = os.path.join(
            settings.PROJECT_ROOT,
            settings.CUSTOM_METADATA_CONFIG_DIR,
            'translations.json'
        )

    try:
        with open(file_path, 'r') as file:
            translations = json.load(file)
        return mark_safe(translations)
    except FileNotFoundError:
        return {}


@register.simple_tag
def test_tag():
    return 'test string'

