base_condition_url = "http://192.168.11.210:3000/api/v1/equipment/{machine}/monitorings/condition/logs?from={begin_datetime}&to={end_datetime}"
base_monitoring_url = "http:/192.168.11.210:3000/api/v1/equipment/{machine}/monitorings/{monitoring}/logs?from={begin_datetime}&to={end_datetime}"
base_rate_url = "http:/192.168.11.210:3000/api/v1/equipment/{machine}/monitorings/rate/logs?from={begin_datetime}&to={end_datetime}"

machine_groups = {
    "Group0001": ['GPH40B', 'INTEGLEXe-420H', 'INTEGLEXj-300', 'INTEGLEXj-400-2', 'LH55N', 'NLX4000-1500MT', 'NLX4000-750', 'NLX6000-2000', 'POWERMASTER-1', 'POWERMASTER-2', 'SLANT-TURN50N', 'V920EX', 'VTM-1200YB'],
    "Group0002": ['SSR-5'],
    "Group0003": ['FH6800','FJV250','INTEGLEXj-400-1', 'MA500', 'MA600H3', 'VARIAXS-i600'],
    "Group0004": ['NVG8T', 'VMG85'],
    "Group0005": ['AJV35-80-1','AJV35-80-2','CVG-9','CVG-9-2','FH680','HCN6800','NHX8000','PRG8DXNC','PSG6DXNC','VCN510C','VM85']
}

monitorings = ['OPERATE', 'DISCONNECT', 'ALARM', 'EMERGENCY','SUSPENDED', 'STOP', 'MANUAL', 'WARMUP', 'WARNING']

equipments_LA = [
    'INTEGLEXe-420H', 'INTEGLEXj-300', 'INTEGLEXj-400-2','LH55N', 
    'NLX4000-1500MT', 'NLX4000-750', 'NLX6000-2000',  
    'POWERMASTER-1', 'POWERMASTER-2', 'SLANT-TURN50N',
    'V920EX', 'VTM-1200YB'
]
equipments_MC = [
    'AJV35-80-1', 'AJV35-80-2', 'FH680', 'FH6800', 'FJV250',
    'HCN6800', 'INTEGLEXj-400-1', 'MA500', 'MA600H3', 'NHX8000',
    'VARIAXS-i600', 'VCN510C'
]
equipments_G = [
    'CVG-9', 'CVG-9-2', 'GPH40B', 'NVG8T',
    'PRG8DXNC', 'PSG6DXNC','SSR-5', 'VMG85', 'VM85'
]

department_dict = {
    'LA': equipments_LA,
    'MC': equipments_MC,
    'G': equipments_G,
    'ALL': equipments_LA + equipments_MC + equipments_G
}

color_dict = {
    'OPERATE': 'green',
    'STOP': 'yellow',
    'ALARM': 'red',
    'EMERGENCY': 'darkred',
    'SUSPENDED': 'orange',
    'MANUAL': 'blue',
    'DISCONNECT': 'gray',
    'WARMUP': 'blue',
    'WARNING': 'lightgray'
}

user_settings = {
    'username': 'User0001',
    'password': '',
}