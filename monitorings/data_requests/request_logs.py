import base64
from datetime import datetime, timedelta, timezone
import os
import requests

import config.settings as settings

class Requestlogs(object):
    
    def __init__(self, username:str=None, password:str=None, machine_groups:dict=None, monitorings:list=None,begin_datetime:datetime=None, end_datetime:datetime=None):
        #read default settings from settings.py
        #url
        self.base_condition_url = settings.base_condition_url
        self.base_monitoring_url = settings.base_monitoring_url
        #認証情報
        self.user_settings = settings.user_settings
        self.default_username = self.user_settings['username']
        self.default_password = self.user_settings['password']
        #機器グループ&モニタリンググループ
        self.default_machine_groups = settings.machine_groups
        self.default_monitorings = settings.monitorings
        #データの取得期間
        self.default_begin_datetime = datetime.now()-timedelta(days=1)
        self.default_end_datetime = datetime.now()

        #ユーザー指定の値
        self.username = username if username is not None else self.default_username
        self.password = password if password is not None else self.default_password
        self.machine_groups = machine_groups if machine_groups is not None else self.default_machine_groups
        self.monitorings = monitorings if monitorings is not None else self.default_monitorings
        self.begin_datetime = begin_datetime if begin_datetime is not None else self.default_begin_datetime
        self.end_datetime = end_datetime if end_datetime is not None else self.default_end_datetime
        self.my_timezone = timezone(timedelta(hours=+9))


    def request_condition_logs(self):
        #機器情報
        machine_groups = self.machine_groups
        #データの取得期間
        begin_datetime = self.begin_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = self.end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        my_timezone = self.my_timezone

        #データを格納するリスト
        condition_logs_list = []

        #機器情報とモニタリンググループを繰り返し処理
        for group, machines in machine_groups.items():
            for machine in machines:
                #APIエンドポイント
                url = self.base_condition_url.format(machine=machine, begin_datetime=begin_datetime, end_datetime=end_datetime)
                #ユーザー名とパスワードをBASE64でエンコード
                credentials = base64.base64encode(f"{self.username}:{self.password}".encode()).decode()

                #header
                headers = {
                    "Content-type": "application.json",
                    "Authorization": f"Basic {credentials}"
                }

                #APIエンドポイントにリクエストを送信
                response = requests.get(url, headers=headers)

                #ステータスコードが200の場合はデータを取得
                if response.status_code == 200:
                    data = response.json()
                    #取得後のデータ処理
                    for item in data:
                        item['machine'] = machine
                        item['group'] = group
                        #UTC時間をJST時間に変換
                        if item["start"] is not None:
                            utc_starttime = datetime.strptime(item["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
                            jst_starttime = utc_starttime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                            item['start'] = jst_starttime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                        if item["end"] is not None:
                            utc_endtime = datetime.strptime(item["end"], "%Y-%m-%dT%H:%M:%S.%fZ")
                            jst_endtime = utc_endtime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                            item["end"] = jst_endtime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                        #データをリストに格納
                        condition_logs_list.append(item)
                else:
                    print(f"エラーが発生しました: {response.status_code}")

        return condition_logs_list

    def request_monitoring_logs(self):
        #機器情報
        machine_groups = self.machine_groups
        #モニタリンググループ
        monitorings = self.monitorings
        #データの取得期間
        begin_datetime = self.begin_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = self.end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        my_timezone = self.my_timezone

        #データを格納するリスト
        monitoring_log_list = []

        #機器情報とモニタリンググループを繰り返し処理
        for group, machines in machine_groups.items():
            for machine in machines:
                #モニタリンググループを繰り返し処理
                for monitoring in monitorings:
                    #APIエンドポイント
                    url = self.base_monitoring_url.format(machine=machine, monitoring=monitoring, begin_datetime=begin_datetime, end_datetime=end_datetime)
                    #ユーザー名とパスワードをbase64でエンコード
                    credentials = base64.base64encode(f"{self.username}:{self.password}".encode()).decode()

                    #header
                    headers = {
                        "Content-type": "application.json",
                        "Authorization": f"Basic {credentials}"
                    }

                    #APIエンドポイントにリクエストを送信
                    response = requests.get(url, headers=headers)

                    #ステータスコードが200の場合はデータを取得
                    if response.status_code == 200:
                        data = response.json()
                        #取得後のデータ処理
                        for item in data:
                            item['machine'] = machine
                            item['group'] = group
                            #UTC時間をJST時間に変換
                            if item["start"] is not None:
                                utc_starttime = datetime.strptime(item["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                jst_starttime = utc_starttime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                                item['start'] = jst_starttime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                            if item["end"] is not None:
                                utc_endtime = datetime.strptime(item["end"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                jst_endtime = utc_endtime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                                item["end"] = jst_endtime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                            #データをリストに格納
                            monitoring_log_list.append(item)
                    else:
                        print(f"エラーが発生しました: {response.status_code}")

        return monitoring_log_list
    
    def save_logs(self, logs_list:list = None, specified_file_name:str=None, specified_folder_path:str=None):
        #ログリストが指定されていない場合はエラーメッセージを送信
        if logs_list is None:
            raise ValueError("logs_list is None")
        else:
            default_file_name = f"logs_{self.begin_datetime.strftime('%Y-%m-%d')}.csv"
            default_folder_path = "./logs"
            file_name = specified_file_name if specified_file_name is not None else default_file_name
            folder_path = specified_folder_path if specified_folder_path is not None else default_folder_path
            file_path = os.path.join(folder_path, file_name)
        logs_df = pl.DataFrame(logs_list)
        logs_df.write_csv("monitoring_logs.csv")
        

        response = requests.get(url, headers=headers)
        if(response.status_code == 200):
            monitoring_log_list.extend(response.json())
        else:
            print(f"error: {response.status_code}")

if __name__ == "__main__":
    request_logs = Requestlogs()
    condition_logs_list = request_logs.request_condition_logs()
    print(condition_logs_list)


