import os
from django.apps import AppConfig
from django.conf import settings


class CustomMetadataConfig(AppConfig):
    name = "custom_metadata"

    def ready(self):
        # inject templates
        settings.TEMPLATES[0]["DIRS"].insert(0, os.path.join(self.path, "templates"))
        run_setup_hooks()


def run_setup_hooks(*args, **kwargs):
    """
    Run basic setup configuration for the custom_metadata app.
    """

    # Add custom URLs
    from django.conf.urls import include, url
    from geonode.urls import urlpatterns

    url_patterns = [
        "datasets",
        "maps",
        "documents",
        "apps",
    ]
    for pattern in url_patterns:
        urlpatterns.insert(
            0,
            url(f"^{pattern}/", include(f"custom_metadata.urls.{pattern}_urls")),
        )

    # Add middleware
    middleware = list(settings.MIDDLEWARE)
    middleware = ["custom_metadata.middleware.AppendMetadataMiddleware"] + middleware
    settings.MIDDLEWARE = tuple(middleware)
