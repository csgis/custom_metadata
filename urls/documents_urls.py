from django.conf.urls import url
from custom_metadata.views import (
    metadata_documents_form_view_decorator,
    metadata_documents_detail_view_decorator,
)

urlpatterns = [
    url(
        r"^(?P<docid>\d+)/metadata$",
        metadata_documents_form_view_decorator,
        name="document_metadata",
    ),
    url(
        r"^(?P<docid>[^/]*)/metadata_detail$",
        metadata_documents_detail_view_decorator,
        name="document_metadata_detail",
    ),
]
