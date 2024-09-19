import os

def get_user_plot_option_dir_path():
    """
    ユーザーがUI上で選択したグラフ描画設定のディレクトリを取得する
    Find for user plot option directory 

    Returns:
        str: user_dir_path
    
    Raises:
        NoUserDirError: If the user directory is not found

    """
    user_dir_path = None

    try:
        import config.settings as settings
        if settings.USER_PLOT_OPTION_DIR_PATH:
            user_dir_path = settings.USER_PLOT_OPTION_DIR_PATH
    except ImportError:
        pass

    if not user_dir_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        user_dir_path = os.path.join(base_dir, "user_dirs")
    return user_dir_path

class NoUserOptionError(Exception):
    pass

def get_user_plot_option_file_path(file_name):
    user_dir_path = get_user_plot_option_dir_path()
    user_file_path = os.path.join(user_dir_path, file_name)
    if not os.path.exists(user_file_path):
        raise NoUserOptionError(f"User plot option file {file_name} not found.")
    return user_file_path

def get_user_setting_list(user_file_path):
    with open(user_file_path, "r", encoding="utf-8") as user_file:
        import json
        settings = json.load(user_file)
        return settings.get("selected_equipments",[])