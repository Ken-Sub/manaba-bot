import os 
import string

def get_template_dir_path():
    """Find bot reply message template's directory path

    Returns:
        str: The template dir path
    """
    template_dir_path = None
    try:
        import core.settings
        template_dir_path = core.settings.BOT_REPLY_MESSAGE_PATH
    except ImportError:
        raise ImportError("core.settings.py file not found")
    
    return template_dir_path

class NoTemplateError(Exception):
    """No Template Error"""
    pass

def find_template(temp_file):
    """Find tempalte file in the given location
    
    Retruns:
        str: the template file path
    
    Raise:
        NoTemplateError: if given template file does not found
    """
    template_dir_path = get_template_dir_path()
    temp_file_path = os.path.join(template_dir_path, temp_file)
    if not temp_file_path:
        raise NoTemplateError("Could not find {}".format(temp_file))

    return temp_file_path

def get_template(temp_file_path):
    """Return bot message template path

    Returns:
        string.Template: Return templates with characters in templates.
    """
    template = find_template(temp_file_path)
    with open(template, 'r') as template_file:
        contents = template_file.read()
        return string.Template(contents) 
