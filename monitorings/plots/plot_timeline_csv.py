from datetime import datetime, timedelta
import os
import time

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import matplotlib.patches as mpatches
import pandas as pd

from config import settings

# 色の設定 全グラフ共通
color_dict = settings.color_dict

#機械の表示順序用リストの設定
equipmentorder_LA = settings.equipments_LA
equipmentorder_MC = settings.equipments_MC
equipmentorder_G = settings.equipments_G

# 機械の表示順序を辞書型で設定 全グラフ共通
equipment_orders = settings.equipment_dict

folder_path = settings.default_folder_path

def calculate_days(file_full_path):
    data = pd.read_csv(file_full_path)
    df = pd.DataFrame(data)
    df = df[df["Kind"]=="condition"]
    df['StartDateTime'] = pd.to_datetime(df['StartDateTime'])
    df['EndDateTime'] = pd.to_datetime(df['EndDateTime'])
    start_time = df['StartDateTime'].min()
    end_time = df['EndDateTime'].max()
    days_diff = (end_time - start_time).days
    return days_diff

def plot_day(day, equipment_order, order_name, file_full_path, folder_path):
    dir_list = []
    path_list = []

    data = pd.read_csv(file_full_path)
    df = pd.DataFrame(data)
    df = df[df["Kind"]=="condition"]
    df['StartDateTime'] = pd.to_datetime(df['StartDateTime'])
    df['EndDateTime'] = pd.to_datetime(df['EndDateTime'])
    # diff列を秒単位で計算
    df['diff'] = (df['EndDateTime'] - df['StartDateTime']).dt.total_seconds()

    start_time = df['StartDateTime'].min()
    carry_over_seconds = {equipment: 0 for equipment in df['EquipmentName'].unique()}

    fig, ax = plt.subplots(figsize=(15, 10))
    day_start = start_time + timedelta(days=day)
    day_end = day_start + timedelta(days=1)
    
    total_seconds_in_day = 24 * 60 * 60  # 1日の秒数

    # データが存在する設備のみをフィルタリング
    valid_equipment_order = [equipment for equipment in equipment_order if not df[(df['EquipmentName'] == equipment) & (df['StartDateTime'] < day_end) & (df['EndDateTime'] > day_start)].empty]

    for i, equipment in enumerate(valid_equipment_order):
        equipment_data = df[(df['EquipmentName'] == equipment) & (df['StartDateTime'] < day_end) & (df['EndDateTime'] > day_start)]
        
        current_time = day_start
        operating_seconds = 0  # 稼働時間の初期値

        #ベクトル化
        start_times = equipment_data['StartDateTime'].apply(lambda x: mdates.date2num(max(x, day_start)))
        end_times = equipment_data['EndDateTime'].apply(lambda x: mdates.date2num(min(x, day_end)))
        contents = equipment_data['Contents']

        #空白の時間をグレーで表示
        empty_durations = start_times - mdates.date2num(current_time)
        empty_mask = current_time < equipment_data['StartDateTime']
        ax.broken_barh([(mdates.date2num(current_time), duration) for duration in empty_durations[empty_mask]], (i - 0.4, 0.8), facecolors=color_dict['Empty'])

        #稼働時間を表示
        durations = end_times - start_times
        
        for start, end, content in zip(start_times, end_times, contents):
            if content in color_dict:
                if end > mdates.date2num(day_end):
                    ax.broken_barh([(start, mdates.date2num(day_end) - start)], (i - 0.4, 0.8), facecolors = color_dict[content])
                    carry_over_seconds[equipment] += (end - mdates.date2num(day_end)) * total_seconds_in_day
                else:
                    ax.broken_barh([(start, end - start)], (i - 0.4, 0.8), facecolors=color_dict[content])
                    carry_over_seconds[equipment] = 0

                if content == "運転中":
                    operating_seconds += (min(end, mdates.date2num(day_end)) - max(start, mdates.date2num(day_start))) * total_seconds_in_day
            
            current_time = min(end, mdates.date2num(day_end))
        
        #最後の状態から翌日の8:00までをグレーで表示
        if current_time < start:
            empty_start = current_time
            empty_duration = start - empty_start
            ax.broken_barh([(empty_start, empty_duration)], (i - 0.4, 0.8), facecolors=color_dict['Empty'])

        # 稼働率の計算と表示
        operating_rate = operating_seconds / total_seconds_in_day * 100
        ax.text(mdates.date2num(day_end) +0.02, i, f'{operating_rate:.2f}%', va='center', fontsize=12)
    
    # 軸の設定
    ax.set_xlim(mdates.date2num(day_start), mdates.date2num(day_end))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    ax.set_yticks(range(len(valid_equipment_order)))
    ax.set_yticklabels(valid_equipment_order)
    plt.xlabel('時間')
    plt.ylabel('機械')

    # タイトルの曜日取得
    weekday_str = day_start.strftime('%A')
    plt.title(f'{order_name} - {day_start.strftime("%Y/%m/%d")} - {weekday_str[:3]}')
    
    # 凡例の設定
    rcParams['font.family'] = 'Meiryo'
    plt.legend(handles=[mpatches.Patch(color=color_dict[key], label=key) for key in color_dict.keys()], loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=10)
    
    plt.tight_layout()
    
    # 保存ディレクトリの作成
    save_dir = os.path.join(folder_path, order_name)
    os.makedirs(save_dir, exist_ok=True)
    # ディレクトリリストに追加
    dir_list.append(save_dir)
    
    # 画像の保存
    save_path = os.path.join(save_dir, f'day_{day_start.strftime("%Y-%m-%d")}.png')
    plt.savefig(save_path)
    plt.close()
    # パスリストに追加
    path_list.append(save_path)
    return dir_list, path_list

dir_path_list = []

rcParams['font.family'] = 'MS Gothic'

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


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    root = tk.Tk()
    root.withdraw()

    while True:
        chosed_file_path = filedialog.askopenfilename(title="CSVデータを選択してください", filetypes=[("CSV", "*.csv")])
        folder_path = os.path.dirname(chosed_file_path)
        if chosed_file_path:
            confirm = messagebox.askyesnocancel("確認", '{}\nこのファイルでグラフを作成しますか？'.format(chosed_file_path.split("/")[-1]))
            if confirm:
                start_time = time.time()
                folder_path = r'C:\Users\nakamura114\Downloads'
                file_full_path = chosed_file_path
                days = calculate_days(file_full_path)
                for order_name, equipment_order in equipment_orders.items():
                    for day in range(days):
                        plot_day(day, equipment_order, order_name, file_full_path, folder_path)
                end_time = time.time()
                messagebox.showinfo("完了", f'実行時間: {end_time - start_time:.2f}秒\nグラフの保存先: {folder_path}')
                break
            elif confirm == False:
                continue
            elif confirm == None:
                root.destroy()
                exit()
        else:
            messagebox.showerror("エラー","ファイルが選択されていません")
            root.destroy()
            exit()
        break
    root.destroy()

if __name__ == '__main__':
    main()