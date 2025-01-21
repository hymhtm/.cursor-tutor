import base64
from datetime import datetime, timedelta, timezone
import os
import requests

import pandas as pd
try:
    from data_requests.config import settings
except ImportError:
    from config import settings

class Requestlogs(object):
    
    def __init__(self, username:str=None, password:str=None, machine_groups:dict=None, monitorings:list=None,begin_datetime:datetime=None, end_datetime:datetime=None):
        #read default settings from settings.py
        #url
        self.base_condition_url = settings.base_condition_url
        self.base_monitoring_url = settings.base_monitoring_url
        #authentication
        self.user_settings = settings.user_settings
        self.default_username = self.user_settings['username']
        self.default_password = self.user_settings['password']
        #machine group & monitoring group
        self.default_machine_groups = settings.machine_groups
        self.default_monitorings = settings.monitorings
        #data acquisition period
        self.default_begin_datetime = datetime.now(timezone.utc)-timedelta(days=1)
        self.default_end_datetime = datetime.now(timezone.utc)

        #user specified value
        self.username = username if username is not None else self.default_username
        self.password = password if password is not None else self.default_password
        self.machine_groups = machine_groups if machine_groups is not None else self.default_machine_groups
        self.monitorings = monitorings if monitorings is not None else self.default_monitorings
        self.begin_datetime = begin_datetime if begin_datetime is not None else self.default_begin_datetime
        self.end_datetime = end_datetime if end_datetime is not None else self.default_end_datetime
        self.my_timezone = timezone(timedelta(hours=+9))


    def request_condition_logs(self):
        #machine information
        machine_groups = self.machine_groups
        #data acquisition period
        begin_datetime = self.begin_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = self.end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        my_timezone = self.my_timezone

        #data storage list
        condition_logs_list = []

        #machine information & monitoring group loop
        for group, machines in machine_groups.items():
            for machine in machines:
                #API endpoint
                url = self.base_condition_url.format(machine=machine, begin_datetime=begin_datetime, end_datetime=end_datetime)
                #user name & password encode
                credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

                #header
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {credentials}"
                }

                #send request to API endpoint
                response = requests.get(url, headers=headers)

                #if status code is 200, get data
                if response.status_code == 200:
                    data = response.json()
                    #data processing after getting data
                    for item in data:
                        item['machine'] = machine
                        item['group'] = group
                        #UTC time to JST time
                        if item["start"] is not None:
                            utc_starttime = datetime.strptime(item["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
                            jst_starttime = utc_starttime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                            item['start'] = jst_starttime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                            
                        if item["end"] is not None:
                            utc_endtime = datetime.strptime(item["end"], "%Y-%m-%dT%H:%M:%S.%fZ")
                            jst_endtime = utc_endtime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                            item["end"] = jst_endtime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                        elif item["end"] is None:
                            item["end"] = datetime.now(my_timezone).strftime("%Y-%m-%d %H:%M:%S.%fZ")
                        #data storage
                        condition_logs_list.append(item)
                else:
                    print(f"エラーが発生しました: {response.status_code}")

        return condition_logs_list


    def request_monitoring_logs(self):
        #machine information
        machine_groups = self.machine_groups
        #monitoring group
        monitorings = self.monitorings
        #data acquisition period
        begin_datetime = self.begin_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = self.end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        my_timezone = self.my_timezone

        #data storage list
        monitoring_log_list = []

        #machine information & monitoring group loop
        for group, machines in machine_groups.items():
            for machine in machines:
                #monitoring group loop
                for monitoring in monitorings:
                    #API endpoint
                    url = self.base_monitoring_url.format(
                        machine=machine, 
                        monitoring=monitoring, 
                        begin_datetime=begin_datetime, 
                        end_datetime=end_datetime
                    )
                    #user name & password encode
                    credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

                    #header
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Basic {credentials}"
                    }

                    #send request to API endpoint
                    response = requests.get(url, headers=headers)

                    #if status code is 200, get data
                    if response.status_code == 200:
                        data = response.json()
                        #data processing after getting data
                        for item in data:
                            item['machine'] = machine
                            item['group'] = group
                            #UTC time to JST time
                            if item["start"] is not None:
                                utc_starttime = datetime.strptime(item["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                jst_starttime = utc_starttime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                                item['start'] = jst_starttime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                            if item["end"] is not None:
                                utc_endtime = datetime.strptime(item["end"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                jst_endtime = utc_endtime.replace(tzinfo=timezone.utc).astimezone(my_timezone)
                                item["end"] = jst_endtime.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                            #data storage
                            monitoring_log_list.append(item)
                    else:
                        print(f"エラーが発生しました: {response.status_code}")

        return monitoring_log_list

    
    def format_logs(self, logs_list:list = None):
        """
        format logs_list to dataframe

        Args:
            logs_list (list, optional): list of json data.

        Returns:
            logs_df: dataframe
        """
        logs_df = pd.DataFrame(logs_list)
        logs_df.columns = ['StartDateTime', 'EndDateTime', 'Contents', 'EquipmentName', 'Group']
        logs_df['StartDateTime'] = pd.to_datetime(logs_df['StartDateTime'])
        logs_df['EndDateTime'] = pd.to_datetime(logs_df['EndDateTime'])
        return logs_df

    
    def save_logs(self, logs_list:list, specified_file_name:str=None, specified_folder_path:str=None):
        """
        save logs_list as a csv file

        Args:
            logs_list (list): list of json data.
            specified_file_name (str, optional): file name.
            specified_folder_path (str, optional): folder path.
        """
        
        if logs_list is None:
            raise ValueError("logs_list is None")
        
        default_file_name = f"logs_{self.begin_datetime.strftime('%Y-%m-%d')}.csv"
        default_folder_path = "./logs"
        file_name = specified_file_name if specified_file_name is not None else default_file_name
        folder_path = specified_folder_path if specified_folder_path is not None else default_folder_path
        
        #create folder if not exist
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = os.path.join(folder_path, file_name)
        logs_df = pd.DataFrame(logs_list)
        logs_df.to_csv(file_path, index=False)


if __name__ == "__main__":
     request_logs = Requestlogs()
     condition_logs_list = request_logs.request_condition_logs()
     request_logs.save_logs(condition_logs_list, specified_file_name=f"condition_logs_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")