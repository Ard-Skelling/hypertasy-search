import sys
from pathlib import Path

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))

from bs4 import BeautifulSoup
from lxml import etree


class Parser:
    def parse_text(self, resp_text):
        soup = BeautifulSoup(resp_text, 'lxml')
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        return text
    
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
