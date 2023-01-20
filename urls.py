from django.conf.urls import url
from .views import decorator_dataset_metadata, decorator_dataset_detail_metadata

urlpatterns = [
    url(r'^(?P<layername>[^/]*)/metadata$',
        decorator_dataset_metadata, name="dataset_metadata"),
    url(r'^(?P<layername>[^/]*)/metadata_detail$',
        decorator_dataset_detail_metadata, name='dataset_metadata_detail'),
]
