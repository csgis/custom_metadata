import json
from django import forms
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_unicode_slug
from typing import Dict, Any, Tuple, List
from datetime import date

# Parse the JSON file
local_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fields.json')
fields_file = getattr(settings, 'METADATA_JSON_DEFINITION', local_file)
with open(fields_file, 'r') as f:
    form_data = json.load(f)

class FormFieldFactory:
    """
    A factory class for creating dynamic form fields based on a JSON definition.
    This factory class maps field types and widgets specified in the JSON definition
    to their corresponding Django form fields and widgets. It also supports setting
    field choices and validators.
    """
    FIELD_MAP: Dict[str, Any] = {
        'CharField': forms.CharField,
        'ChoiceField': forms.ChoiceField,
        'DateField': forms.DateField,
        'BooleanField': forms.BooleanField,
        'RadioSelectField': forms.ChoiceField,
        'NumberField': forms.IntegerField,
    }
    WIDGET_MAP: Dict[str, Any] = {
        'TextInput': forms.TextInput,
        'Select': forms.Select,
        'CheckboxInput': forms.CheckboxInput,
        'TextArea': forms.Textarea,
        'HiddenInput': forms.HiddenInput,
        'DatePicker': forms.DateInput(attrs={'type': 'date'}),
        'RadioSelect': forms.RadioSelect
    }

    def create_field(self, type: str, name: str, label: str, required: bool, widget: str, choices: Tuple[Tuple[str, str]]):
        field = self.FIELD_MAP.get(type)(label=label, required=required)
        widget_class = self.WIDGET_MAP.get(widget)
        if widget_class:
            if widget == 'DatePicker':
                field.widget = widget_class
            else:
                field.widget = widget_class()
        if type == 'ChoiceField' or type == 'RadioSelectField':
            field.choices = choices
        field.validators.append(validate_unicode_slug)
        return field


class CreateExtraMetadataForm(forms.Form):
    """
    A form for creating extra metadata.
    """
    def __init__(self, json_data=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        factory = FormFieldFactory()
        self.initial_metadata = kwargs.get('initial')
        json_file_data = json_data['fields'] if json_data else form_data['fields']

        # create form fields for fields that have a json definition
        api_only_fields = self.add_api_data_to_json_fields(json_file_data)
        json_file_data = json_file_data + api_only_fields

        # create form fields for fields that have a json definition
        for form_item in json_file_data:
            form_input_copy = form_item.copy()
            field_choices = form_input_copy.get('choices', None)
            if field_choices:
                field_choices = [(choice['value'], choice['label']) for choice in field_choices]
                del form_input_copy['choices']
            name = form_input_copy.get('name')
            self.fields[name] = factory.create_field(choices=field_choices, **form_input_copy)


    def is_valid(self) -> bool:
        self.cleaned_data = {}
        self._errors = {}
        for field_name, field in self.fields.items():
            if field_name in self.initial_metadata:
                field_value = self.initial_metadata.get(field_name)
                if isinstance(field, forms.CharField):
                    field = forms.CharField(max_length=255)
                    field.widget = forms.TextInput()
                elif isinstance(field, forms.DateField):
                    field = forms.DateField()
                    field.widget = forms.DateInput()
                elif isinstance(field, forms.ChoiceField):
                    field = forms.ChoiceField(choices=field.choices)
                    field.widget = forms.Select()
                try:
                    self.cleaned_data[field_name] = field.clean(field_value)
                    #print(f"getting {field_name}")
                except forms.ValidationError as error:
                    print(f"{field_name} failed")
                    self._errors[field_name] = error.messages
        return not bool(self._errors)

    def add_api_data_to_json_fields(self, json_file_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add fields from the API data that are not present in the json definition file to the json fields.

        Args:
            json_file_data: A list of field definitions in json format.

        Returns:
            A list of field definitions in json format that includes fields added from the API data.
        """

        all_fields_of_json_definition_file = [item['name'] for item in json_file_data]
        all_fields_added_by_api = list(self.initial.keys())
        api_only_metadata_fields = [i for i in all_fields_added_by_api if i not in all_fields_of_json_definition_file]
        api_only_fields = []

        for field in api_only_metadata_fields:
            new_char_field = {
                    "type": "CharField",
                    "name": field,
                    "label": field,
                    "required": False,
                    "widget": "TextInput"
                }
            api_only_fields.append(new_char_field)
        return api_only_fields

    def json_serial(self, obj):
        if isinstance(obj, (date)):
            return obj.isoformat()
        else:
            return obj

    def save(self, layer, ExtraMetadata):
        md_to_update = self.cleaned_data
        resources = layer.metadata.all().delete()
        for k in md_to_update.keys():
            k = k.replace("gn__emd-","")
            json_metadata = {k: self.json_serial(md_to_update[k])}
            extra_meta = ExtraMetadata.objects.create(resource=layer, metadata=json_metadata)
            layer.metadata.add(extra_meta)
