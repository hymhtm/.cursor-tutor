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

user_settings = {
    'username': 'User0001',
    'password': '',
}
