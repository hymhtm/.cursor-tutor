class NoConfigFileError(Exception):
    pass

def get_user_setting_list():
    """
    Find user setting list
    and if not found, create new empty list

    Returns:
        list: user_setting_list
    
    Raises:
        NoConfigFileError: If the config file is not found
    """

def save_user_setting_list(user_setting_list)