import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time

import report_output_day_collector as rodc
import plot_monthly_pivot as pmp
import pivot_styler as ps

def main():
    root = tk.Tk()
    root.withdraw()

    while True:
        chosed_folder_path = filedialog.askdirectory(title= "フォルダを選択してください")
        if os.path.exists(chosed_folder_path):
            confirm = messagebox.askyesnocancel(title="確認", message="{}\nのデータを読み込みますか？".format(chosed_folder_path))
            if confirm:
                start_time = time.time()
                dataframe = rodc.collect_xlsdata(chosed_folder_path)
                file_path = pmp.create_pivot_table(dataframe, chosed_folder_path)
                ps.pivot_styler(file_path)
                end_time = time.time()
                elapsed_time = end_time - start_time
                messagebox.showinfo(title="完了", message="実行時間: {:.2f}秒".format(elapsed_time))
                break
            elif confirm is False:
                continue
            else:
                break
            break
        else:
            messagebox.showerror("エラー", "フォルダが存在しません")
            break
        break
    root.destroy()

if __name__ == '__main__':
    main()