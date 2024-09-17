from datetime import timedelta
import os
import xlrd
import pandas as pd
from config import settings

'''
folder_path: フォルダのパス

'''
def collect_xlsdata(folder_path):
    file_list = []
    folder_path = folder_path

    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xls'):
                file_list.append(os.path.join(folder_path, file))

    sec_dataframe = pd.DataFrame()

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

        df.drop(df[df.index=='１日累計'].index, axis=0, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)
    
        df['設備名'] = sheet.cell_value(0,3)
        
        df['Timestamp'] = pd.to_datetime(file[-12:-4] + str(' 08:00:00'))
        df['Date'] =  df['Timestamp'].dt.date - timedelta(days=1)
        sec_dataframe = pd.concat([sec_dataframe, df], ignore_index=False)
    
    sec_dataframe.reindex(columns=['設備名', 'Timestamp','Date', '運転中', '停止中', 'アラーム中', '非常停止中', '手動運転中', '一時停止中', '切断中'])
    sec_dataframe.to_excel(os.path.join(folder_path, 'sec_data.xlsx'), index=True)
    return sec_dataframe