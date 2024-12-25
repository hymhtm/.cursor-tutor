base_condition_url = "http://192.168.11.210:3000/api/v1/equipment/{machine}/monitorings/condition/logs?from={begin_datetime}&to={end_datetime}"
base_monitoring_url = "http:/192.168.11.210:3000/api/v1/equipment/{machine}/monitorings/{monitoring}/logs?from={begin_datetime}&to={end_datetime}"
base_rate_url = "http:/192.168.11.210:3000/api/v1/equipment/{machine}/monitorings/rate/logs?from={begin_datetime}&to={end_datetime}"

machine_groups = {
    "Group0001": ['VTM-1200YB', 'NLX4000-1500MT', 'INTEGLEXe-420H', 'INTEGLEXj-400-2', 'NLX4000-750', 'INTEGLEXj-300', 'NLX6000-2000', 'V920EX', 'GPH40B', 'LH55N', 'PSG6DXNC'],
    "Group0002": ['SSR-5'],
    "Group0003": ['INTEGLEXj-400-1', 'FH6800', 'MA600H3', 'MA500', 'VARIAXS-i600'],
    "Group0004": ['NVG8T', 'VMG85'],
    "Group0005": ['HCN6800', 'FH680', 'NHX8000', 'VM85', 'PSG6DXNC', 'CVG-9']
}

monitorings = ['OPERATE', 'DISCONNECT', 'ALARM', 'EMERGENCY','SUSPENDED', 'STOP', 'MANUAL', 'WARMUP', 'WARNING']

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

department_dict = {
    'LA': equipments_LA,
    'MC': equipments_MC,
    'G': equipments_G,
    'ALL': equipments_LA + equipments_MC + equipments_G
}

color_dict = {
    '運転中': 'green',
    '停止中': 'yellow',
    'アラーム中': 'red',
    '非常停止中': 'darkred',
    '一時停止中': 'orange',
    '手動運転中': 'blue',
    '切断中': 'gray',
    '待機中': 'blue',
    'Empty': 'lightgray'
}

user_settings = {
    'username': 'User0001',
    'password': '',
}