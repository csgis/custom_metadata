from django.conf.urls import url
from custom_metadata.views import (
    metadata_apps_form_view_decorator,
    metadata_apps_detail_view_decorator,
)

urlpatterns = [
    url(
        r"^(?P<geoappid>\d+)/metadata$",
        metadata_apps_form_view_decorator,
        name="geoapp_metadata",
    ),
    url(
        r"^(?P<geoappid>[^/]*)/metadata_detail$",
        metadata_apps_detail_view_decorator,
        name="geoapp_metadata_detail",
    ),
]
