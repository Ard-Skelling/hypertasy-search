'''
Author: anzaikk 599957546@qq.com
Date: 2023-05-10 20:44:08
LastEditors: anzaikk 599957546@qq.com
LastEditTime: 2023-05-11 13:02:59
FilePath: /hypertasy-search/utils/utils.py
Description: utils工具
'''
import hashlib
# import zoneinfo
# import datetime

def encrypted_password(pwd, salt):
    md5_obj = hashlib.md5()
    md5_obj.update(salt.encode("utf-8"))
    md5_obj.update(pwd.encode("utf-8"))
    return md5_obj.hexdigest()

def get_md5(text):
    return hashlib.md5().hexdigest()

# def get_now():
#     tz = zoneinfo.ZoneInfo("Asia/Shanghai")
#     now = datetime.datetime.now(tz)
#     return now