#API取得関連情報
machine_groups = {
    "Group0001": ['VTM-1200YB', 'NLX4000-1500MT', 'INTEGLEXe-420H', 'INTEGLEXj-400-2', 'NLX4000-750', 'INTEGLEXj-300', 'NLX6000-2000', 'V920EX', 'GPH40B', 'LH55N', 'PSG6DXNC'],
    "Group0002": ['SSR-5'],
    "Group0003": ['INTEGLEXj-400-1', 'FH6800', 'MA600H3', 'MA500', 'VARIAXS-i600'],
    "Group0004": ['NVG8T', 'VMG85'],
    "Group0005": ['HCN6800', 'FH680', 'NHX8000', 'VM85', 'PSG6DXNC', 'CVG-9']
}

monitorings = ['OPERATE', 'DISCONNECT', 'ALARM', 'EMERGENCY','SUSPENDED', 'STOP', 'MANUAL', 'WARMUP', 'WARNING']
monitoring_dict = {'OPERATE': '運転中', 'DISCONNECT': '切断中', 'ALARM': 'アラーム中', 'EMERGENCY': '非常停止中', 'SUSPENDED': '一時停止中', 'STOP': '停止中', 'MANUAL': '手動運転中', 'WARMUP': '暖機運転中', 'WARNING': '警告'}


#デフォルトの色設定
color_dict = {
    'アラーム中': 'red', 
    '非常停止中': 'darkred', 
    '運転中': 'green', 
    '停止中': 'yellow', 
    '一時停止中': 'orange', 
    '手動運転中': 'blue', 
    '切断中': 'gray', 
    '待機中': 'blue', 
    'Empty': 'lightgray'
}

# デフォルトの機械の表示順序
equipments_LA = [
    'NLX6000-2000', 'LH55N', 'VTM-1200YB', 'NLX4000-750', 
    'INTEGLEXj-300', 'V920EX', 'NLX4000-1500MT', 
    'INTEGLEXe-420H', 'INTEGLEXj-400-2','POWERMASTER-1',
    'POWERMASTER-2','SLANT-TURN50N'
]
equipments_MC = [
    'MA600H3', 'MA500', 'VARIAXS-i600', 'INTEGLEXj-400-1', 
    'FH6800', 'HCN6800', 'FH680', 'NHX8000', 'FJV250',
    'AJV35-80-1','AJV35-80-2'
]
equipments_G = [
    'SSR-5', 'GPH40B', 'VMG85', 'NVG8T', 'CVG-9', 'CVG-9-2', 'VM85',
    'PSG6DXNC','PRG8DXNC'
]

equipment_dict = {
    'LA': equipments_LA,
    'MC': equipments_MC,
    'G': equipments_G
}

default_folder_path = 'C:/Users/user/Downloads/'

#ユーザーのデフォルト設定
user_settings = {
    'username': 'User0001',
    'password': '',
    'color_dict': color_dict,
    'equipment_dict': equipment_dict,
    'folder_path': default_folder_path
}
