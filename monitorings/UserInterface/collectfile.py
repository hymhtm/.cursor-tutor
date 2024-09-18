import os
import time
import pandas as pd
import openpyxl as opxl
import xlrd

import config.settings as settings


dir_path = settings.dir_path
file_path = os.path.join(dir_path, "execution_time.txt")

# 前回の実行時間を読み込む
with open(file_path, 'r') as file:
    last_execution_time = float(file.read().strip())

# フォルダ内のファイルをリストアップ
folder_path = dir_path
files = os.listdir(folder_path)

# 前回の実行時間以降に作成されたファイルをピックアップ
new_files = [file for file in files if os.path.getctime(os.path.join(folder_path, file)) > last_execution_time]

# 新しいファイルのリストを表示（または他の処理を行う）

for file in new_files:
    # 日報ファイルのファイル名から機械名と日付を抽出
    machine_name = ""
    date = ""
    if(file[:17] == "report_output_Day"):
        machine_name = file[18:-13]
        date = file[-12:-4]
        print(f"機械名: {machine_name}, 日付: {date}")
        
        file_path = os.path.join(folder_path, file)
        if(file_path.endswith(".xlsx")):
            df = pd.read_excel(file_path, header=8,engine='openpyxl')  # 9行目からデータを読み込む
        elif(file_path.endswith(".xls")):
            df = pd.read_excel(file_path, header=8,engine='xlrd')  # 9行目からデータを読み込む
        else:
            print(f"スキップ：{file} はサポートされていない形式です。※")
            continue
        # 必要なデータを抽出
        try:
            df = df[['運転中時間', '停止中時間', 'アラーム中時間', '非常停止中時間', '手動運転中時間', '一時停止中時間', '切断中時間']]
            df['機械名'] = machine_name
            df['日付'] = date
        except KeyError as e:
            print("エラー: 指定されたカラムが見つかりません。", e)
            print("現在のDataFrameのカラム:", df.columns)
                
        # データを時系列データに変換
        
        #dfをエクセルファイルとして保存
        df.to_excel(os.path.join(dir_path, f"{machine_name}_{date}.xlsx"), index=False)

# 現在の実行時間を保存
with open(file_path, 'w') as file:
    file.write(str(time.time()))