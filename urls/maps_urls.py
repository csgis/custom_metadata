from django.conf.urls import url
from custom_metadata.views import (
    metadata_map_form_view_decorator,
    metadata_map_detail_view_decorator,
)

urlpatterns = [
    url(
        r"^(?P<mapid>[^/]+)/metadata$",
        metadata_map_form_view_decorator,
        name="map_metadata",
    ),
    url(
        r"^(?P<mapid>[^/]*)/metadata_detail$",
        metadata_map_detail_view_decorator,
        name="map_metadata_detail",
    ),
]
