import requests
import base64
import polars as pl
from datetime import datetime, timedelta, timezone
import settings

#認証情報
username = settings.username
password = settings.password

#機器グループ&モニタリンググループ
machine_groups = settings.machine_groups
monitorings = settings.monitorings

class request_monitoring_log:
    

