import requests
import base64
from datetime import datetime, timedelta, timezone
import config.settings

#認証情報
username = config.settings.username
password = config.settings.password

#機器グループ&モニタリンググループ
machine_groups = config.settings.machine_groups
monitorings = config.settings.monitorings