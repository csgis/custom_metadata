import json
import os
from django.conf import settings


def read_config_from_json(resource_type: str) -> dict:
    """
    Read the metadata fields configuration from a json file for a specific resource type.

    :param resource_type: The type of resource for which the configuration is being read.
    :return: The JSON content of the configuration file for the specified resource type.
    """

    fields_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "custom_metadata",
        "metadata_fields",
        f"{resource_type}_fields.json",
    )

    if hasattr(settings, "CUSTOM_METADATA_CONFIG_DIR"):
        fields_file = os.path.join(
            settings.CUSTOM_METADATA_CONFIG_DIR,
            f"{resource_type}_fields.json",
        )


    try:
        with open(fields_file, "r") as f:
            json_file_content = json.load(f)
            return json_file_content
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the config file for {resource_type} in {fields_file}.")
