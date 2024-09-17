from datetime import datetime, timedelta
import json
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import matplotlib.patches as mpatches
import pandas as pd
import polars as pl

class Plot(object):
    """
    Plotクラスは、指定されたファイルパスと機械設備の順序に基づいてデータをプロットするためのクラスです。

    Attributes:
        file_full_path (str): データファイルのフルパス。
        equipment_order (list): 機器の順序。
        order_name (str, optional): オーダー名。デフォルトはNone。

    Methods:
        __init__(file_full_path, equipment_order, order_name=None):
            初期化メソッド。ファイルパス、機器の順序、およびオーダー名を設定します。
        
        plot_operating_result(day):
            指定された日の稼働推移をプロットします。
        
        plot_operating_rate(day):
            指定された日の稼働率をプロットします。
    
    """
    def __init__(self, config_path='config.json'):
        try:
            #read config.json
            with open(config_path, 'r') as f:
                config = json.load(f)    
            self.default_user_settings = config['user_settings']
            self.default_color_dict = self.default_user_settings['color_dict']
            self.default_folder_path = self.default_user_settings['folder_path']
            self.default_equipment_orders = self.default_user_settings['equipment_orders']

        except FileNotFoundError:
            import settings
            #read settings
            self.default_user_settings = settings.user_settings
            self.default_folder_path = settings.folder_path
            self.default_color_dict = settings.color_dict
            self.default_equipment_orders = settings.equipment_dict

        rcParams['font.family'] = 'MS Gothic'


    def plot_day(self, day):


        #get usersettings
        user_settings = self.default_user_settings #get usersettings
        equipment_orders = user_settings['equipment_orders'] #get equipment orders
color_dict = user_settings['color_dict'] #get color dict
folder_path = user_settings['folder_path'] #get folder path

#graph settings
subplot_kwargs = {'nrows': 1, 'ncols': 1, 'figsize': (12, 6)}

#set font
rcParams['font.family'] = 'MS Gothic'

#save plot function
def save_plot(file_path, folder_path, order_name):
    save_dir = os.path.join(folder_path, order_name)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file_path)
    plt.savefig(save_path)
    plt.close()


def plot_day(file_full_path, equipment_order, order_name):
    file_list = []

    data = pd.read_csv(file_full_path)
    df = pd.DataFrame(data)
    df = df[df["Kind"]=="condition"]
    df['StartDateTime'] = pd.to_datetime(df['StartDateTime'])
    df['EndDateTime'] = pd.to_datetime(df['EndDateTime'])

    # diff列を秒単位で計算
    df['diff'] = (df['EndDateTime'] - df['StartDateTime']).dt.total_seconds()

    start_time = df['StartDateTime'].min()
    end_time = start_time + timedelta(days=7)
    carry_over_seconds = {equipment: 0 for equipment in df['EquipmentName'].unique()}

    fig, ax = plt.subplots(figsize=(15, 10))
    day_start = start_time + timedelta(days=day)
    day_end = day_start + timedelta(days=1)
    
    total_seconds_in_day = 24 * 60 * 60  # 1日の秒数
    for i, equipment in enumerate(equipment_order):
        equipment_data = df[(df['EquipmentName'] == equipment) & (df['StartDateTime'] < day_end) & (df['EndDateTime'] > day_start)]
        current_time = day_start
    
    
    
        operating_seconds = 0  # 稼働時間の初期値
        carry_over = carry_over_seconds[equipment]  # 前日の超過分を初期値に設定

        for _, row in equipment_data.iterrows():
            start = mdates.date2num(max(row['StartDateTime'], day_start))
            end = mdates.date2num(min(row['EndDateTime'], day_end))

            # 空白の時間をグレーで表示
            if current_time < row['StartDateTime']:
                empty_start = mdates.date2num(current_time)
                empty_duration = start - empty_start
                ax.broken_barh([(empty_start, empty_duration)], (i - 0.4, 0.8), facecolors=color_dict['Empty'])

            duration = end - start
            # 'Contents'列が存在するか確認
            if 'Contents' in row:
                if row['EndDateTime'] > day_end:
                    # 超過分の処理
                    excess_start = mdates.date2num(day_end)
                    excess_duration = end - excess_start
                    ax.broken_barh([(start, mdates.date2num(day_end) - start)], (i - 0.4, 0.8), facecolors=color_dict[row['Contents']])
                    carry_over_seconds[equipment] += (row['EndDateTime'] - day_end).total_seconds()
                else:
                    ax.broken_barh([(start, duration)], (i - 0.4, 0.8), facecolors=color_dict[row['Contents']])
                    carry_over_seconds[equipment] = 0

                if row['Contents'] == '運転中' or row['Contents'] == 'AUTO CYCLE':
                    operating_seconds += (min(row['EndDateTime'], day_end) - max(row['StartDateTime'], day_start)).total_seconds()

            else:
                print(f"Warning: 'Contents' column not found in row: {row}")

            # current_timeの更新
            current_time = min(row['EndDateTime'], day_end)
        
        # 最後の状態から翌日の8:00までをグレーで表示
        if current_time < day_end:
            empty_start = mdates.date2num(current_time)
            empty_duration = mdates.date2num(day_end) - empty_start
            ax.broken_barh([(empty_start, empty_duration)], (i - 0.4, 0.8), facecolors=color_dict['Empty'])
        
        # 稼働率の計算と表示
        operating_rate = operating_seconds / total_seconds_in_day * 100
        ax.text(mdates.date2num(day_end) +0.02, i, f'{operating_rate:.2f}%', va='center', fontsize=12)
    
    # 軸の設定
    ax.set_xlim(mdates.date2num(day_start), mdates.date2num(day_end))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    ax.set_yticks(range(len(equipment_order)))
    ax.set_yticklabels(equipment_order)
    plt.xlabel('Time')
    plt.ylabel('Machine')

    # タイトルの曜日取得
    weekday_str = day_start.strftime('%A')
    plt.title(f'{order_name} - {day_start.strftime("%Y/%m/%d")} - {weekday_str[:3]}')
    
    # 凡例の設定
    rcParams['font.family'] = 'Meiryo'
    plt.legend(handles=[mpatches.Patch(color=color_dict[key], label=key) for key in color_dict.keys()], loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=10)
    
    plt.tight_layout()
    default_file_name = f'{order_name} - day_{day_start.strftime("%Y-%m-%d")} - {weekday_str[:3]}.png'
    file_list.append(default_file_name)
    return file_list


for order_name, equipment_order in equipment_orders.items():
    for day in range(7):
        plot_day(day, equipment_order, order_name)

dir_path_list = []

'''
for dir in dir_list:
    dir_path = os.path.join(folder_path, dir)
    dir_path_list.append(dir_path)
'''

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

plot_rate(folder_path)


