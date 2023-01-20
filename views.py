from django.conf import settings
from django.http import HttpResponse
from geonode.base.models import ExtraMetadata
from geonode.layers.views import dataset_metadata, dataset_metadata_detail, _resolve_dataset, _PERMISSION_MSG_METADATA
import json
from .dynamic_form import CreateExtraMetadataForm
from datetime import date
import os

def custom_metadata_decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
        layer = _resolve_dataset(
            request,
            kwargs.get('layername'),
            'base.change_resourcebase_metadata',
            _PERMISSION_MSG_METADATA
        )
        if request.method == 'POST':
            response = view_func(request, *args, **kwargs)
            if response.status_code == 200:
                data={k.replace('gn__emd-',''): request.POST[k] for k in request.POST if k.startswith("gn__emd")}
                form = CreateExtraMetadataForm(initial=data, prefix='gn__emd')

                if form.is_valid():
                    md_to_update = form.cleaned_data
                    form.save(layer, ExtraMetadata)
                else:
                    print(form.data)
                    print(form.errors.items())
                    for field_name, errors in form.errors.items():
                        if errors:
                            print(f'{field_name} field has errors: {errors}')

                    if form.non_field_errors():
                        print(form.non_field_errors())

            #return response
            return HttpResponse("ok")
        else:
            # Add the extra metadata to the context
            custom_metadata = {}
            try:
                resources = layer.metadata.all()
                for resource in resources:
                    if isinstance(resource.metadata, str):
                        data = json.loads(resource.metadata)
                    else:
                        data = resource.metadata
                    if data:
                        custom_metadata.update(data)
            except Exception as e:
                print(e)

            form = CreateExtraMetadataForm(initial=custom_metadata, prefix='gn__emd')
            template = 'custom_metadata/custom_panels.html'
            panel_template = getattr(settings, 'PANEL_TEMPLATE', template)
            response = view_func(request,
                                *args,
                                panel_template=panel_template,
                                custom_metadata=form,
                                **kwargs)
            return response

    return _wrapped_view

def custom_metadata_detail_decorator(view_func):
    def decorator_func(request, layername, *args, **kwargs):
        template = 'custom_metadata/custom_dataset_metadata_detail.html'
        response = view_func(request, layername, template=template)
        return response
    return decorator_func

decorator_dataset_metadata = custom_metadata_decorator(dataset_metadata)
decorator_dataset_detail_metadata = custom_metadata_detail_decorator(dataset_metadata_detail)
