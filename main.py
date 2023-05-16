'''
Author: anzaikk 599957546@qq.com
Date: 2023-05-09 14:29:24
LastEditors: anzaikk 599957546@qq.com
LastEditTime: 2023-05-16 13:46:33
FilePath: /hypertasy-search/main.py
Description: 程序入口
'''
from module import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8003, reload=True)