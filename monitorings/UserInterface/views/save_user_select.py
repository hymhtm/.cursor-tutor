import json

class NoConfigFileError(Exception):
    pass


def get_user_setting_list(user_setting_file_path):
    """
    Find user setting list
    and if not found, create new empty list

    Returns:
        list: user_setting_list
    
    Raises:
        NoConfigFileError: If the config file is not found
    """
    try:
        with open(user_setting_file_path, "r") as f:
            user_setting_file = json.load(f)
    except NoConfigFileError:
        raise NoConfigFileError("No config file found")
    return user_setting_file

def save_user_setting_list(user_setting_list):
    """
    Save user setting list

    Args:
    
        user_setting_list (list): user setting list
    """
    try:
        with open(user_setting_file_path, "w") as f:
            json.dump(user_setting_list, f)
    except NoConfigFileError:
        raise NoConfigFileError("No config file found")
    