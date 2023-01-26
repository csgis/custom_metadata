.. title: About

About
=====

GeoNode's metadata model is based on the ISO 19115 standard. This standard defines the structure and content of metadata for geographic information and is widely used in the spatial data community. The standard includes information such as resource title, summary, keywords, spatial and temporal extent and contact information.

However, there is often a need to add custom metadata to layers or maps.

What can this app do for you?
-----------------------------

This app extends 
  - the metadata wizard with freely definable form fields
  - the metadata detail view of a resource
  - the XML export of a dataset
  - creates form fields for data added by the REST API

This is how the Wizard looks like with extra fields

.. image:: https://user-images.githubusercontent.com/20478652/214605375-d7bf3520-ff14-4708-88de-229319b7579c.jpeg
   :scale: 50

Currently available fields
--------------------------

The app currently offers following input fields
  * NumberField
  * CharField
  * DateField (with a calendar picker)
  * RadioSelectField
  * BooleanField

and following widgets:
  * TextInput
  * Select
  * CheckboxInput
  * TextArea
  * HiddenInput
  * DatePicker
  * RadioSelect

  
