import os
import openpyxl
from pandas import pivot_table
from config import settings
from resolve_path import resolve_path

def create_pivot_table(dataframe, folder_path):
    path = resolve_path(folder_path)
    df = dataframe
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'PivotTable'

    # ピボットテーブルを作成
    df['運転中'] = df['運転中'].astype(int) / 86400
    pivot = pivot_table(df, values='運転中', index=['Date'], columns=['設備名'], aggfunc='sum',fill_value=0,)

    # ピボットテーブルをExcelファイルに出力
    return_path = os.path.join(path, 'monthly_pivot_table.xlsx')
    pivot.to_excel(return_path, index=True)
    return return_path