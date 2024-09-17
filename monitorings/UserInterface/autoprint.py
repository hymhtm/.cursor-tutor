import ctypes
from ctypes import wintypes
import os
import win32print

dir_list = [r"C:\Users\nakamura114\Desktop\LA", r"C:\Users\nakamura114\Desktop\MC", r"C:\Users\nakamura114\Desktop\G"]
#テスト用folder_path
folder_path = dir_list[0]

for roots, dirs, files in os.walk(folder_path):
    file_list = []
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            file_list.append(file)
    print(file_list)

winspool= ctypes.WinDLL(os.path.join(os.environ['SystemRoot'], 'System32', 'winspool.drv'))

PRINTER_ENUM_LOCAL = 0x00000002

class PRINTER_INFO_2(ctypes.Structure):
    _fields_ = [
        ("pServerName", wintypes.LPWSTR),
        ("pPrinterName", wintypes.LPWSTR),
        ("pShareName", wintypes.LPWSTR),
        ("pPortName", wintypes.LPWSTR),
        ("pDriverName", wintypes.LPWSTR),
        ("pComment", wintypes.LPWSTR),
        ("pLocation", wintypes.LPWSTR),
        ("pDevMode", wintypes.LPVOID),
        ("pSepFile", wintypes.LPWSTR),
        ("pPrintProcessor", wintypes.LPWSTR),
        ("pDatatype", wintypes.LPWSTR),
        ("pParameters", wintypes.LPWSTR),
        ("pSecurityDescriptor", wintypes.LPVOID),
        ("Attributes", wintypes.DWORD),
        ("Priority", wintypes.DWORD),
        ("DefaultPriority", wintypes.DWORD),
        ("StartTime", wintypes.DWORD),
        ("UntilTime", wintypes.DWORD),
        ("Status", wintypes.DWORD),
        ("cJobs", wintypes.DWORD),
        ("AveragePPM", wintypes.DWORD)
    ]

def get_default_printer():
    size_needed = wintypes.DWORD()
    winspool.GetDefaultPrinterW(None, ctypes.byref(size_needed))
    buffer = ctypes.create_unicode_buffer(size_needed.value)
    if winspool.GetDefaultPrinterW(buffer, ctypes.byref(size_needed)):
        return buffer.value
    else:
        raise ctypes.WinError()


def print_confirm(hWnd):

    result = ctypes.windll.user32.MessageBoxW(hWnd, "印刷しますか？", "確認",0x00000001)
    if result == 1:
        print("印刷します")
        return True
    elif result == 2:
        print("印刷を中止しました")
        return False
    else:
        print("キャンセルしました")
        return False

def print_file(print_confirm, file_path):
    if print_confirm:
        winspool = ctypes.WinDLL(os.path.join(os.environ['SystemRoot'], 'System32', 'winspool.drv'))
        file_path = os.path.abspath(file_path)

        default_printer = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(default_printer)
        ctypes.windll.winspool.OpenPrinter(ctypes.c_wchar_p(default_printer), ctypes.pointer(hPrinter), None)
    else:
        print("印刷を中止しました")

print_file(print_confirm(None), r"C:\Users\nakamura114\Desktop\claude3 API key.txt")