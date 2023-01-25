import json
import os
from django.conf import settings


def read_config_from_json(resource_type: str) -> dict:
    """
    Read the metadata fields configuration from a json file for a specific resource type.

    :param resource_type: The type of resource for which the configuration is being read.
    :return: The JSON content of the configuration file for the specified resource type.
    """
    try:
        local_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"metadata_fields/{resource_type}_fields.json",
        )
        fields_file = getattr(settings, "METADATA_MAP_JSON_DEFINITION", local_file)
        print("using json file: ", fields_file)
        with open(fields_file, "r") as f:
            json_file_content = json.load(f)
            return json_file_content
    except FileNotFoundError:
        raise os.FileNotFoundError(
            f"Could not find the config file for {resource_type}."
        )
