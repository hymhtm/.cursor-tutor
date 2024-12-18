import os
import xlrd

import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as mpatches
import pandas as pd

folder_path = r"C:\Users\nakamura114\Downloads\Report"
#dir_list = ['LA', 'MC', 'G']
#folder_path = r"C:\Users\nakamura114\Downloads\drive-download-20240618T073919Z-001"
dir_path_list = []

rcParams['font.family'] = 'MS Gothic'

'''
for dir in dir_list:
    dir_path = os.path.join(folder_path, dir)
    dir_path_list.append(dir_path)
'''
color_dict = {'アラーム中': 'red', '非常停止中':'darkred', '運転中': 'green', '停止中': 'yellow', '一時停止中': 'orange', '切断中': 'gray', '待機中': 'blue', 'Empty': 'lightgray', '手動運転中': 'blue'}

#graph settings
subplot_kwargs = {'nrows': 1, 'ncols': 1, 'figsize': (12, 6)}

def autopct_format(values):
    def my_format(pct):
        return('%.1f%%' % pct) if pct >= 0.05 else ''
    return my_format

#plot function
def plot_rate(folder_path):
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
    
    tmpdata.to_csv(os.path.join(folder_path, 'rate_data.csv'), index=False)

    grouped = tmpdata.groupby('設備名')

    grouped.to_csv(os.path.join(folder_path, 'grouped_rate_data.csv'), index=False)

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

if __name__ == '__main__':
    folder_path = r"C:\Users\nakamura114\Downloads\Report\Report\report_output_monthly"
    plot_rate(folder_path)