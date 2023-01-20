import os
from django.apps import AppConfig
from django.conf import settings

class CustomMetadataConfig(AppConfig):
    name = 'custom_metadata'

    def ready(self):
        pass
        '''
        This part is here for reference.
        Warning! It is not a good idea to dynamicully update settings
        as it makes it makes the settings hard to understand!
        '''

        '''
        # Inject custom templates to geonode Templates dir.
        # Doing so you can override existing
        dirs = list(settings.TEMPLATES[0]['DIRS'])
        settings.TEMPLATES[0]['DIRS'].insert(0, os.path.join(self.path, 'templates'))

        # Inject Middleware or app templates in geonode core
        dirs = list(settings.TEMPLATES[0]['DIRS'])
        settings.TEMPLATES[0]['DIRS'].insert(0, os.path.join(self.path, 'templates'))
        custom_metadata_middleware = 'custom_metadata.middleware.AboutMiddleware'
        MIDDLEWARE = list(settings.MIDDLEWARE)
        MIDDLEWARE.append(custom_metadata_middleware)
        settings.MIDDLEWARE = MIDDLEWARE
        '''
