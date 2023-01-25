import json
import logging
import os
from datetime import date

from django.conf import settings
from django.http import HttpResponse

from geonode.base.models import ExtraMetadata
from geonode.layers.views import (
    _PERMISSION_MSG_METADATA,
    _resolve_dataset,
    dataset_metadata,
    dataset_metadata_detail,
)

from geonode.maps.views import map_metadata, map_metadata_detail, _resolve_map, _PERMISSION_MSG_VIEW
from geonode.documents.views import document_metadata, document_metadata_detail
from geonode.geoapps.views import geoapp_metadata, geoapp_metadata_detail

from .dynamic_form import CreateExtraMetadataForm
from .get_item_config import get_config_obj
from .config_reader import read_config_from_json
from .response_handlers import handle_response
from .resolve_resource import resolve_resource_type

log = logging.getLogger("django")


def handle_generic_metadata_detail(view_func):
    def decorator_func(request, *args, **kwargs):
        # Currently there is only one generic template, this could be extended to  allow
        # templates per page
        template = "custom_metadata/custom_generic_metadata_detail.html"
        response = view_func(request, *args, template=template, **kwargs)
        return response

    return decorator_func


def handle_generic_metadata_form(view_func):
    def _wrapped_view(request, *args, **kwargs):

        config_obj = get_config_obj(request)
        resource = resolve_resource_type(request, config_obj, kwargs)
        json_file_content = read_config_from_json(config_obj["type"])

        # The data needs to be saved. We process the POST data and pass
        # it to the CreateExtraMetadataForm class
        if request.method == "POST":
            response = view_func(request, *args, **kwargs)
            if response.status_code == 200:

                # prepare the post data an remove the prefix
                # this should be automaticully done by prefix='gn__emd'?
                data = {
                    k.replace("gn__emd-", ""): request.POST[k]
                    for k in request.POST
                    if k.startswith("gn__emd")
                }

                form = CreateExtraMetadataForm(
                    json_file_content, initial=data, prefix="gn__emd"
                )

                if form.is_valid():
                    form.save(resource, ExtraMetadata)
                else:
                    for field_name, errors in form.errors.items():
                        if errors:
                            log.error(f"{field_name} field has errors: {errors}")
                    if form.non_field_errors():
                        log.error(form.non_field_errors())
                    # Todo: Error reporting should be improved
                    return HttpResponse("There was an Eror updating the resource")

            return response
            # return HttpResponse("Resource updated")
        elif request.method == "GET":
            # Populate the model data and add the extra metadata to the context
            form_custom_metadata = {}
            try:
                resources = resource.metadata.all()
                for resource in resources:
                    obj = resource.metadata
                    if not isinstance(resource.metadata, dict):
                        continue
                    if "name" not in obj or "value" not in obj:
                        continue
                    # The metadata json is expected to have name and value keys
                    data = {obj["name"]: obj["value"]}
                    form_custom_metadata.update(data)
            except Exception as e:
                log.error(e)

            # Build the form
            form = CreateExtraMetadataForm(
                json_file_content, initial=form_custom_metadata, prefix="gn__emd"
            )
            template = config_obj.get("panels_template", None)
            # Todo: Allow settings override of different template types
            panel_template = getattr(settings, "PANEL_TEMPLATE", template)
            # return html object
            return handle_response(
                request, view_func, config_obj, panel_template, form, *args, **kwargs
            )

        else:
            # method not handled by decorator
            return handle_response(
                request, view_func, config_obj, panel_template, form, *args, **kwargs
            )

    return _wrapped_view


# layer
metadata_dataset_form_view_decorator = handle_generic_metadata_form(dataset_metadata)
metadata_dataset_detail_view_decorator = handle_generic_metadata_detail(
    dataset_metadata_detail
)

# maps
metadata_map_form_view_decorator = handle_generic_metadata_form(map_metadata)
metadata_map_detail_view_decorator = handle_generic_metadata_detail(
    map_metadata_detail
)

# documents
metadata_documents_form_view_decorator = handle_generic_metadata_form(document_metadata)
metadata_documents_detail_view_decorator = handle_generic_metadata_detail(
    document_metadata_detail
)

# apps
metadata_apps_form_view_decorator = handle_generic_metadata_form(geoapp_metadata)
metadata_apps_detail_view_decorator = handle_generic_metadata_detail(
    geoapp_metadata_detail
)