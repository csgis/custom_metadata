Configuration
==============

Django settings
----------------

After installing the app via github or pip (not yet supported), it must be registered in the Django settings like any other app:

.. code-block::
        INSTALLED_APPS = (
            ...
            "custom_metadata.apps.CustomMetadataConfig",
            ...
        )

.. code-block:: python

    INSTALLED_APPS = (
    ...
    "custom_metadata.apps.CustomMetadataConfig",
    ...
    )

next activate the plugin in your settings with

.. code-block:: python

    EXTRA_METADATA_ENABLED = os.getenv("EXTRA_METADATA_ENABLED", True)


Define your forms for different resources
-----------------------------------------

The plugin generates the forms from JSON definitions. For each resource type (dataset, map, document, geoapp [dashboard, geostory]) a separate JSON definition must be created.

The naming convention is:

- datasets -> dataset_fields.json
- maps -> map_fields.json
- documents -> document_fields.json
- geoapps -> app_fields.json

Examples can be found in the folder custom_metadata/metadata_fields.

Here `dataset_fields.json` shows all form fields available at the time.

.. code-block:: json

  {
      "fields": [
          {
              "type": "NumberField",
              "name": "age",
              "label": "Age",
              "required": false,
              "widget": "TextInput"
          },
          {
              "type": "CharField",
              "name": "planet",
              "label": "Planet",
              "required": false,
              "widget": "TextInput"
          },
          {
              "type": "DateField",
              "name": "discovered_Data",
              "label": "Discovered date",
              "required": false,
              "widget": "DatePicker"
          },
          {
              "type": "RadioSelectField",
              "name": "size_of_planet",
              "label": "Size of planet",
              "required": true,
              "widget": "RadioSelect",
              "choices": [
                  {"value":"small", "label":"Small"},
                  {"value":"medium", "label":"Medium"},
                  {"value":"large", "label":"Large"}
              ]
          },
          {
              "type": "BooleanField",
              "name": "is_published",
              "label": "Is published",
              "required": false,
              "widget": "CheckboxInput"
          },
          {
              "type": "CharField",
              "name": "percent_of_water",
              "label": "Percent of water",
              "required": false,
              "widget": "TextInput"
          },
          {
              "type": "ChoiceField",
              "name": "relevance",
              "label": "Relevance of planet",
              "choices": [
                  {"value":"Food", "label":"Food"},
                  {"value":"Water", "label":"Water"},
                  {"value":"Fun", "label":"fun"}
              ],
              "required": false,
              "widget": "Select"
          }
      ]
  }

which would render a form for a dataset as

.. image:: https://user-images.githubusercontent.com/20478652/214805447-771d0257-9d8a-48b3-8463-75456b8651c9.jpeg
   :scale: 50


Customize XML output
--------------------

The app extends the Geonode XML output of datasets (known as layer in older versions) with the metadata of the resource. The output of the data can be customised in the template file custom_metadata/templates/full_metadata.xml.

The relevant code block is

.. code-block:: html

       <gmd:AdditionalData>
       {% for extra in layer.extra_metadata %}
         {% for key, value in extra.items %}
           {% with key=key|valid_xml_element %}
               <gmd:{{ key }}>{{ value }}</gmd:{{ key }}>
           {% endwith %}
         {% endfor %}
       {% endfor %}
     </gmd:AdditionalData>

Customize HTML output
---------------------

Metatada Wizard
................

Die HTML Ausgabe des neuen Metadaten Schritt erfolgt in custom_metdata/*_panels.html. für datasets zum Beispiel:

custom_metadata/templates/dataset_panel.html

.. code-block:: html

  {% extends "layouts/panels.html" %}
  {% load i18n %}

  {% block extra_metadata_steps%}
  <li data-step="5" data-toggle="tab" href="#extra_metadata">
    <a>{% trans "Extra Metadata" %}</a>
   </li>
  {% endblock %}

  {% block extra_metadata_content %}
  <div id="extra_metadata" class="tab-pane fade">
      <div class="panel-group"><div class="panel panel-default"><div class="panel-body">
        <div>
          <div style="padding: 15px; ">
              {{ custom_metadata.as_p }}
            </div>
          </div>
        </div>
      </div>
    </div>
  {% endblock %}

  {% block dataset_abstract %}
      {{ block.super }}<br>
  {% endblock %}

  {% block layer_extra_metadata %}
  {% endblock %}

- extra_metadata_steps definiert den zusätzlichen Menüpunkt.
- extra_metadata_content renders the form that the app generates from the respective JSON definition.
- dataset_abstract is an example if you want to output the form in an existing item.
- layer_extra_metadata overwrites the existing implementation of GeoNode. This is mandatory for the operation of the app.

.. image:: https://user-images.githubusercontent.com/20478652/214805447-771d0257-9d8a-48b3-8463-75456b8651c9.jpeg
   :scale: 50

Metdata detail
...............

The adjustments to the metadata detail view are made in custom_metadata/templates/custom_generic_metadata_detail.html.
The ouput can easily be customized by changing the jinja2 loop:

.. code-block:: html

  {% extends "metadata_detail.html" %}

  {% block extra_metadata %}
    {% if resource.extra_metadata %}
      {% for extra in resource.extra_metadata %}
        {% for key, value in extra.items %}
            <dt>{{ key }}</dt>
            <dd>{{ value }}</dd>
        {% endfor %}
      {% endfor %}
    {% endif %}
  {% endblock extra_metadata %}

is interpreted as:

.. image:: https://user-images.githubusercontent.com/20478652/214811947-b795a309-eb6b-45f7-a3e9-b09077acae34.jpeg
   :scale: 50

This file is currently used for all resource types.



