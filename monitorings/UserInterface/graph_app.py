import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from monitorings.UserInterface.config.settings import user_settings

color_dict = user_settings['color_dict']
equipment_orders = user_settings['equipment_orders']

#ファイルの選択
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSVファイル", "*.csv"), ("XLSファイル", "*.xls")])
    if file_path:
        label.config(text=file_path)
        dir_path = os.path.dirname(file_path)
        return file_path, dir_path
    else:
        label.config(text="ファイルを選択してください")

#フォルダの選択
def choose_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        label.config(text=folder_path)
    else:
        label.config(text="フォルダを選択してください")


#グラフの選択
def choose_plot():
    graph
    msgbox = tk.messagebox
    if graph_type != "稼働推移" or graph_type != "稼働率":
        msgbox.showinfo("エラー", "グラフが正しく選択されていません")
    else:
        return graph_type

def on_closing():
    messagebox = tk.messagebox
    if messagebox.askokcancel("確認", "グラフ描画を終了しますか？"):
        root.destroy()

def on_coding():
    messagebox = tk.messagebox
    messagebox.showinfo("作成中", "未実装の機能です")

#グラフの描画
def plot_graph(file_path ,dir_path, graph_type):
    if graph_type == "稼働推移":
        from plots import plot_day
        plot_day(file_path, save_dir=dir_path, equipment_order=e)
        plot_timeline(file_path, )
    elif graph_type == "稼働率":
        from plot_rate import plot_rate
        plot_rate(file_path)

def customize_colors():
    for status in color_dict.keys():
        color = colorchooser.askcolor(title=f"Choose color for {status}")[1]
        if color:
            color_dict[status] = color


def customize_order():
    global equipment_orders
    new_order = {}
    for key, value in equipment_orders.items():
        new_order[key] = simpledialog.askstring("Input", f"Enter new order for {key} (comma separated):", initialvalue=",".join(value)).split(",")
    equipment_orders = new_order

'''
def make_original_equipment_order():
    from plot_timeline import equipment_orders
    return equipment_orders
'''

root = tk.Tk()
root.title("グラフを作成する")
root.geometry("1366x768")

menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="file", command=select_file)
file_menu.add_command(label="edit data", command=on_coding) #後で関数作成予定
file_menu.add_command(label="close", command=on_closing)

graph_menu = tk.Menu(menubar, tearoff=0)
graph_menu.add_command(label="plot graph", command=choose_plot)
graph_menu.add_command(label="save graph", command=on_coding) #後で関数作成予定

menubar.add_cascade(label='file', menu=file_menu)
menubar.add_cascade(label='graph', menu=graph_menu)


frame = tk.Frame(root, width=500, height=300)
frame.pack_propagate(0)
frame.pack(padx=10, pady=10)

label_frame = ttk.LabelFrame(frame, width=500, height=200)
label_frame.pack(padx=10, pady=10)

label = ttk.Label(label_frame, text="ファイルを選択してください")
label.pack()
button = ttk.Button(label_frame, text="ファイルを選択", command=select_file)
button.pack()

label_frame2 = ttk.LabelFrame(frame, width=500, height=400)
label_frame2.pack(padx=10, pady=10)

label2 = ttk.Label(label_frame2, text="グラフの種類を選択してください")
label2.pack()

graph_type = tk.StringVar()
radiobutton_1 = ttk.Radiobutton(label_frame2, text="稼働推移", variable=graph_type, value="稼働推移")
radiobutton_2 = ttk.Radiobutton(label_frame2, text="稼働率", variable=graph_type, value="稼働率")
#entry = ttk.Entry(frame, width=30)

plot_button = ttk.Button(label_frame2, text="グラフを作成",command=choose_plot)

radiobutton_1.pack()
radiobutton_2.pack()
plot_button.pack()

progressbar = ttk.Progressbar(frame, orient='horizontal', length=200, mode='determinate')
progressbar.pack()

#entry.pack()

#スタイルを設定
style = ttk.Style()
style.configure("TFrame", background="lightgrey")
style.configure("TLabel", font=("Meiryo", 12))
style.configure("TButton", background="White", padding=6, relief="solid")
#style.configure("TEntry", background="lightgrey", font=("Arial", 14))
style.configure("TRadiobutton", font=("Arial", 12))

root.mainloop()