import flet as ft

import monitorings.UserInterface.config.default_settings as default_settings
from monitorings.UserInterface.views.search_dirs import get_template

def main(page: ft.Page):
    page.title = "稼働グラフ作成ツール"
    greeting = get_template("top.txt")
    page.controls.append(ft.Text(value=greeting, color="blue"))

    equipment = default_settings.equipment_dict
    
    for department, machine_list in equipment.items():
        page.controls.append(ft.Text(value=department, color="blue"))
    page.update()

ft.app(target=main)