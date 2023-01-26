Development
============

This document explains the program flow in case you plan to contribute.

URLs
....

The app overwrites the route defined in geonode depending on the resource/app. Responsible for this are the url definitions in custom_metadata/urls


View decorators
...............

The views defined here can be found in custom_metadata/views.py
Currently there are two generic views that "decorate" the original views in geonode.

.. code-block:: txt
  custom_metadata.views.handle_generic_metadata_detail

A deocrator view responsible for feeding the matdata detail view with its own template.

.. code-block:: txt

 custom_metadata.views.handle_generic_metadata_form

A decorator view responsible for feeding a custom Django form into the context for GET requests. It also updates the m2m relation of the resource base model for POST requests.

Helpers
........

.. code-block:: txt

  custom_metadata.dynamic_form.CreateExtraMetadataForm

Generates the Django form enriched with data from the database.

.. code-block:: txt

  custom_metadata.get_item_config.GetItemConfig

Sets the appropriate configuration based on the called URL (defines the app).

.. code-block:: txt

  custom_metadata.resolve_resource.resolve_resource_type

Reads the matching resource from the database based on the type. (used by handle_generic_metadata_form)

.. code-block:: txt

  custom_metadata.get_item_config.GetItemConfig

Selects the right "return" object matching the app (decorated by the handle_generic_metadata_form).


Templates
.........

The customized templates can be found in

custom_metadata/templates

Form defintions
................
The json based Django Form definitions can be found in

custom_metadata/metadata_fields


