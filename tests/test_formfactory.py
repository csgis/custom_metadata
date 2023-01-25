from custom_metadata.dynamic_form import FormFieldFactory, CreateExtraMetadataForm
from django import forms
from unittest import mock, TestCase

# TODO:
# This tests are similar. One testing only the Factory the other
# the __ini__ method as well. Both are not needed by the chosen should be
# improved


class FilterTests(TestCase):
    @mock.patch("django.db.utils.ConnectionHandler.__getitem__")
    def test_create_field(self, mock_getitem):
        factory = FormFieldFactory()
        field = factory.create_field(
            type="CharField",
            name="username",
            label="Username",
            required=True,
            widget="TextInput",
            choices=None,
        )
        self.assertIsInstance(field, forms.CharField)
        self.assertEqual(field.label, "Username")
        self.assertEqual(field.required, True)
        self.assertIsInstance(field.widget, forms.TextInput)


class CreateExtraMetadataFormTests(TestCase):
    def test_init(self):
        # mock form data
        form_data = {
            "fields": [
                {
                    "type": "CharField",
                    "name": "username",
                    "label": "Username",
                    "required": True,
                    "widget": "TextInput",
                },
                {
                    "type": "ChoiceField",
                    "name": "gender",
                    "label": "Gender",
                    "choices": [
                        {"value": "male", "label": "Male"},
                        {"value": "female", "label": "Female"},
                    ],
                    "required": True,
                    "widget": "Select",
                },
            ]
        }

        # create an instance of the form and initialize it
        form = CreateExtraMetadataForm(
            json_file_content=form_data, initial=None, prefix="gn__emd"
        )

        # check if the form fields are created correctly
        self.assertIn("username", form.fields)
        field = form.fields["username"]
        self.assertIsInstance(field, forms.CharField)
        self.assertEqual(field.label, "Username")
        self.assertIsInstance(field.widget, forms.TextInput)

        self.assertIn("gender", form.fields)
        field = form.fields["gender"]
        self.assertIsInstance(field, forms.ChoiceField)
        self.assertEqual(field.label, "Gender")
        self.assertTrue(field.required)
        self.assertIsInstance(field.widget, forms.Select)
