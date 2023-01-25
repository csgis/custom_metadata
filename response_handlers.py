from typing import Type, Dict, Any

class ResponseHandler:
    def handle(
        self, request, view_func, config_obj, panel_template, form, *args, **kwargs
    ) -> Any:
        pass


class MapHandler(ResponseHandler):
    def handle(
        self, request, view_func, config_obj, panel_template, form, *args, **kwargs
    ) -> Any:
        return view_func(
            request,
            kwargs.get("mapid"),
            panel_template=panel_template,
            custom_metadata=form,
        )


class DatasetHandler(ResponseHandler):
    def handle(
        self, request, view_func, config_obj, panel_template, form, *args, **kwargs
    ) -> Any:
        return view_func(
            request,
            *args,
            panel_template=panel_template,
            custom_metadata=form,
            **kwargs
        )


class DocumentHandler(ResponseHandler):
    def handle(
        self, request, view_func, config_obj, panel_template, form, *args, **kwargs
    ) -> Any:
        return view_func(
            request,
            *args,
            panel_template=panel_template,
            custom_metadata=form,
            **kwargs
        )

class AppHandler(ResponseHandler):
    def handle(
        self, request, view_func, config_obj, panel_template, form, *args, **kwargs
    ) -> Any:
        return view_func(
            request,
            *args,
            panel_template=panel_template,
            custom_metadata=form,
            **kwargs
        )

class DefaultHandler(ResponseHandler):
    def handle(
        self, request, view_func, config_obj, panel_template, form, *args, **kwargs
    ) -> Any:
        # Does it make sense to offer a Default return?
        raise NotImplementedError("The DefaultHandler should not be used for handling the response.")


def handle_response(
    request,
    view_func: callable,
    config_obj: Dict[str, Any],
    panel_template: str,
    form: Any,
    *args,
    **kwargs
) -> Any:
    handler_mapping: Dict[str, Type[ResponseHandler]] = {
        'map': MapHandler,
        'dataset': DatasetHandler,
        'document': DocumentHandler,
        'app': AppHandler,
    }
    handler_class = handler_mapping.get(config_obj['type'], DefaultHandler)
    return handler_class().handle(
        request, view_func, config_obj, panel_template, form, *args, **kwargs
    )
