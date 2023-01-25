from typing import Callable
from django.urls import resolve
import re


class GetItemConfig:
    """
    Class that handles the configuration of different types of resources,
    such as maps, datasets, and documents.
    """

    def __init__(self, strategies_map: dict):
        """
        Initializes the GetItemConfig class with a dictionary of strategies.

        :param strategies_map: A dictionary mapping resource types to their
        corresponding configuration methods.
        """
        self._strategies = strategies_map

    def handle_request(self, strategy: str) -> dict:
        if strategy not in self._strategies:
            return "URL not found"
        return self._strategies[strategy]()

    @classmethod
    def is_map(cls) -> dict:
        resource_type_return_obj = {
            "type": "maps",
            "panels_template": "custom_metadata/maps_panels.html",
        }
        return resource_type_return_obj

    @classmethod
    def is_dataset(cls) -> dict:
        resource_type_return_obj = {
            "type": "datasets",
            "panels_template": "custom_metadata/datasets_panels.html",
        }
        return resource_type_return_obj

    @classmethod
    def is_document(cls) -> dict:
        resource_type_return_obj = {
            "type": "document",
            "panels_template": "custom_metadata/documents_panels.html",
        }
        return resource_type_return_obj


def get_type_by_first_url_folder(request):
    """
    Extract the first folder in the request url and use it to identify the resource type.
    :param request: request object
    :return: str
    """
    match = re.search(r"^https?:\/\/[^\/]+(\/[^\/]+).*$", request.get_raw_uri())
    # maybe raise error instead of fallback
    strategy = match.group(1).split("/")[1] if match else "datasets"
    return strategy


def get_config_obj(request):
    """
    Return the config object for the request url
    :param request: request object
    :return: dict
    """
    strategies_map = {
        "maps": GetItemConfig.is_map,
        "datasets": GetItemConfig.is_dataset,
        "document": GetItemConfig.is_document,
    }

    strategy = get_type_by_first_url_folder(request)
    url_handler = GetItemConfig(strategies_map)
    document_type_return_obj = url_handler.handle_request(strategy)
    return document_type_return_obj
