'''
Author: anzaikk 599957546@qq.com
Date: 2023-05-06 20:54:22
LastEditors: anzaikk 599957546@qq.com
LastEditTime: 2023-05-11 18:52:16
FilePath: /hypertasy-search/module/parser.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
from fastapi import UploadFile
import re

from pathlib import Path

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))

from bs4 import BeautifulSoup
import pdfplumber


class Parser:

    @staticmethod
    def parse_document(document: UploadFile):
        document = document.file
        text = ""
        with pdfplumber.open(document) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def parse_text(resp_text):
        soup = BeautifulSoup(resp_text, 'lxml')
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        return text
    
    @staticmethod
    def split_text(text, max_length=1024):
        paragraphs = text.split("\n")
        current_length = 0
        current_chunk = []

        for paragraph in paragraphs:
            if current_length + len(paragraph) + 1 <= max_length:
                current_chunk.append(paragraph)
                current_length += len(paragraph) + 1
            else:
                yield "\n".join(current_chunk)
                current_chunk = [paragraph]
                current_length = len(paragraph) + 1

        if current_chunk:
            yield "\n".join(current_chunk)


    def create_message(chunk, question):
        return {
            "prompt": f'"""# 内容开始\n{chunk}\n# 内容结束"""\n根据上述内容, 回答下面的问题: "{question}" -- 如果上述内容不能用于回答问题, 总结上述内容。以“回答：...\n依据：...”的形式返回结果'
        }

if __name__ == '__main__':
    import requests

    url = 'https://developer.aliyun.com/article/1073999'
    r = requests.get(url)

    parser = Parser()
    res = parser.parse_text(r.text)
    print(res)
