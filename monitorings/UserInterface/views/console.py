import os
import string

def get_template_dir_path():
    template_dir_path = None
    try:
        import config.settings as settings
        if settings.TEMPLATE_DIR_PATH:
            template_dir_path = settings.TEMPLATE_DIR_PATH
    except ImportError:
        pass

    if not template_dir_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir_path = os.path.join(base_dir, "templates")
    
    return template_dir_path


class NoTemplateError(Exception):
    pass

def find_template(temp_file_name):
    template_dir_path = get_template_dir_path()
    template_file_path = os.path.join(template_dir_path, temp_file_name)
    if not os.path.exists(template_file_path):
        raise NoTemplateError(f"Template file {temp_file_name} not found.")
    return template_file_path

def get_template(template_file_name):
    template_file_path = find_template(template_file_name)
    with open(template_file_path, "r", encoding="utf-8") as template_file:
        contents = template_file.read()
        contents = contents.rstrip()
        return contents


def get_setting_dir_path():
    setting_dir_path = None
    try:
        import config.settings as settings
        if settings.SETTING_DIR_PATH:
            setting_dir_path = settings.SETTING_DIR_PATH
    except ImportError:
        pass

    if not setting_dir_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        setting_dir_path = os.path.join(base_dir, "settings")
    
    return setting_dir_path

class NoSettingError(Exception):
    pass

def find_setting(setting_file_name):
    setting_dir_path = get_setting_dir_path()
    setting_file_path = os.path.join(setting_dir_path, setting_file_name)
    if not os.path.exists(setting_file_path):
        raise NoSettingError(f"Setting_file {setting_file_name} not found.")
    return setting_file_path

def get_setting(setting_file_name):
    setting_file_path = find_setting(setting_file_name)
    with open(setting_file_path, "r", encoding="utf-8") as setting_file:
        contents = setting_file.read()
        contents = contents.rstrip()
        return contents