import os
import sys
import time

import flet as ft

from monitorings.plots.config import settings
from monitorings.plots import plot_timeline_csv
from monitorings.plots import report_output_day_collector
from monitorings.plots import plot_monthly_pivot
from monitorings.plots import pivot_styler
from views.console import get_template

def main(page: ft.Page):
    page.title = "稼働グラフ作成ツール"
    greeting = get_template("top.txt")
    page.controls.append(ft.Text(value=greeting, color="blue"))

    equipment = settings.equipment_dict
    
    for department, machine_list in equipment.items():
        page.controls.append(ft.Text(value=department, color="blue"))
    page.update()

ft.app(target=main)