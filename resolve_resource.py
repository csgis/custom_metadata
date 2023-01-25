# -*- coding: utf-8 -*-
from geonode.maps.views import map_metadata, _resolve_map, _PERMISSION_MSG_VIEW
# Todo: Decide if private variables and functions should really be used
from geonode.layers.views import (
    _PERMISSION_MSG_METADATA,
    _PERMISSION_MSG_GENERIC,
    _resolve_dataset,
    dataset_metadata,
    dataset_metadata_detail,
)
from typing import Dict
from geonode.documents.views import _resolve_document
from geonode.geoapps.views import _resolve_geoapp


class ResourceType:
    def resolve(self, request: object, kwargs: Dict) -> object:
        raise NotImplementedError


class MapResourceType(ResourceType):
    def resolve(self, request: object, kwargs: Dict) -> object:
        return _resolve_map(
            request,
            kwargs.get("mapid"),
            "base.change_resourcebase_metadata",
            _PERMISSION_MSG_VIEW,
        )


class DatasetResourceType(ResourceType):
    def resolve(self, request: object, kwargs: Dict) -> object:
        return _resolve_dataset(
            request,
            kwargs.get("layername"),
            "base.change_resourcebase_metadata",
            _PERMISSION_MSG_METADATA,
        )

class DocumentReourceType(ResourceType):
    def resolve(self, request: object, kwargs: Dict) -> object:
        return _resolve_document(
            request,
            kwargs.get("docid"),
            "base.change_resourcebase",
            msg=_PERMISSION_MSG_GENERIC,
        )

class AppReourceType(ResourceType):
    def resolve(self, request: object, kwargs: Dict) -> object:
        return _resolve_geoapp(
            request,
            kwargs.get("geoappid"),
            permission="base.change_resourcebase",
            msg=_PERMISSION_MSG_GENERIC
        )


def resolve_resource_type(request: object, config_obj: Dict, kwargs: Dict) -> object:
    resource_type_mapping = {
        "map": MapResourceType(),
        "dataset": DatasetResourceType(),
        "document": DocumentReourceType(),
        "app": AppReourceType(),
    }

    resource_type_handler = resource_type_mapping.get(config_obj["type"], None)
    if resource_type_handler is None:
        # TODO: Handle the case where config_obj['type'] is not in the mapping
        pass
    else:
        resource_type = resource_type_handler.resolve(request, kwargs)
        return resource_type
