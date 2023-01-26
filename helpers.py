import os

def get_templates_path():
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(current_file_path, 'templates')
    print(templates_path)