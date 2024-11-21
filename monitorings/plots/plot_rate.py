from datetime import timedelta
import importlib.util
import os
import sys
import time

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import matplotlib.patches as mpatches
import pandas as pd

#from config import settings

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 色の設定 全グラフ共通
settings_path = resource_path(os.path.join('monitorings', 'plots', 'config', 'settings.py'))
spec = importlib.util.spec_from_file_location("settings", settings_path)
settings = importlib.util.module_from_spec(spec)
spec.loader.exec_module(settings)
color_dict = settings.color_dict

#機械の表示順序用リストの設定
equipmentorder_LA = settings.equipments_LA
equipmentorder_MC = settings.equipments_MC
equipmentorder_G = settings.equipments_G

# 機械の表示順序を辞書型で設定 全グラフ共通
equipment_orders = settings.equipment_dict

folder_path = settings.default_folder_path

#graph settings
subplot_kwargs = {'nrows': 1, 'ncols': 1, 'figsize': (12, 6)}

def autopct_format(values):
    def my_format(pct):
        return('%.1f%%' % pct) if pct >= 0.05 else ''
    return my_format

#plot function
def plot_rate(folder_path):
    import xlrd
    file_list = []
    folder_path = folder_path

    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xls'):
                #file_list.append(os.path.join(roots, file))
                file_list.append(os.path.join(folder_path, file))

    tmpdata = pd.DataFrame()

    for file in file_list:
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_name('DATA')
        data = []
        for row in range(10, sheet.nrows):
            row_data = sheet.row_values(row, start_colx = 0, end_colx = 9)
            data.append(row_data)
    
        df = pd.DataFrame(data)
        df.columns = sheet.row_values(8, start_colx=0, end_colx=9)
        df.index = sheet.col_values(0, start_rowx=10, end_rowx=sheet.nrows)
        df = df.drop(df.columns[:2], axis=1)
        df.drop(df[df.index=='1日累計'].index, axis=0, inplace=True)
        df['設備名'] = sheet.cell_value(0,3)
        
        df['Timestamp'] = pd.to_datetime(file[-12:-4] + str(' 08:00:00'))

        tmpdata = pd.concat([tmpdata, df], axis=0)

    grouped = tmpdata.groupby('設備名')

    # グラフを描画
    for name, group in grouped:
        fig, ax = plt.subplots(**subplot_kwargs)
        summary = group[['運転中', '停止中', 'アラーム中', '非常停止中', '手動運転中', '一時停止中', '切断中']].sum()
        date = group['Timestamp'].min().strftime('%Y-%m-%d')
        ax.pie(summary, colors =[color_dict[status] for status in summary.index], autopct=autopct_format(summary), startangle=90)
        ax.set_title(f'{date} {name} の稼働率')
        ax.axis('equal')
        ax.legend(handles=[mpatches.Patch(color=color_dict[status], label=status) for status in summary.index], bbox_to_anchor=(0.7, 0), ncols=4)
        plt.tight_layout()

        save_dir = folder_path
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        plt.savefig(os.path.join(save_dir, f'{date} - {name}.png'))
        plt.close()
