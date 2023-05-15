import sys
from pathlib import Path

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))

import requests, asyncio
from typing import Union, List, Dict
from fastapi import FastAPI, Request, UploadFile, Form
from pydantic import BaseModel
from module.parser import Parser
from module.summary import summarize_text, get_final_answer, fast_summarize, one_one_simi
from data_storage import RedisClient
from utils import get_md5
from fastapi.middleware.cors import CORSMiddleware

# TODO: authentication

class PostData(BaseModel):
    question: str = ''
    url:str = ''
    text:str = ''

    class Config:
        extra = 'ignore'

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	# 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
	allow_origins=["*"],
	# 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
	allow_credentials=False,
	# 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
	allow_methods=["*"],
	# 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
	# 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
	allow_headers=["*"],
	# 可以被浏览器访问的响应头, 默认是 []，一般很少指定
	# expose_headers=["*"]
	# 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
	# max_age=1000
)

class WebTask(BaseModel):
    url: str

    class Config:
        extra = 'allow'

CRAWLER_URL = 'http://39.104.82.158:8002'
NLP_URL = 'http://39.104.82.158:8001'
INDEX_URL = CRAWLER_URL + '/bing_spider/search'
SEARX_URL = 'http://54.151.16.174:8888/search'
DETAIL_URL = CRAWLER_URL + '/play_spider/request'


def get_ems(sentences):
    ...

@app.post('/john_chat/chat_text')
async def john_chat_text(post_data: PostData):
    text = post_data.text
    question = post_data.question
    # 暂时计算，后面交由前端完成
    c_ems_md5 = get_md5(text)

    # 解析文本出结果
    summary = fast_summarize(text, question, c_ems_md5)
    return summary


@app.post('/john_chat/chat_url')
async def john_chat_url(post_data: PostData):
    url = post_data.url
    question = post_data.question

    # 暂时计算，后面交由前端完成
    c_ems_md5 = get_md5(url)

    if not (c_ems_string := RedisClient().conn.get(c_ems_md5)):
        task = {'url': url}
        form = {
            'tasks': task
        }
        resp = requests.post(DETAIL_URL, json=form)
        document = resp.json()[0]['content']

        # 解析文本出结果
        content = Parser.parse_text(document)
        RedisClient().conn.set(c_ems_md5 + "url", content, ex=700)

    else:
        content = RedisClient().conn.get(c_ems_md5 + "url").decode('utf-8')
    # summary = summarize_text(content, question)
    summary = fast_summarize(content, question, c_ems_md5)
    
    return summary


@app.post('/john_chat/chat_document')
# document 参数使用UploadFile后面支持更多扩展
async def john_chat(document:UploadFile, question:str=Form()):
    # 解析文本出结果
    content = Parser.parse_document(document)
    # 暂时计算，后面交由前端完成
    c_ems_md5 = get_md5(content)
    # summary = summarize_text(content, question)
    summary = fast_summarize(content, question, c_ems_md5)
    return summary


@app.get('/john_search/')
async def john_search(request: Request):
    query = request.query_params.get('q')
    question = request.query_params.get('question')
    engine = request.query_params.get('engine')

    if engine == 'searx':
        params = {'q': query, 'format': 'json'}
        res = requests.get(SEARX_URL, params=params)
        res = res.json()
        res = res['results']
        if not res:
            return '无可奉告，还是另请高明吧。'
        result = [{'url': r.get('pretty_url')} for r in res if r.get('pretty_url')]
    else:
        params = {'q': query}
        res = requests.get(INDEX_URL, params=params)
        res = res.json()
        result = res['result']

    form = {'tasks': result}
    res = requests.post(DETAIL_URL, json=form)
    res = res.json()
    parser = Parser()
    summaries = []
    if not question:
        question = query
    for ta in res:
        content = parser.parse_text(ta['content'])
        url = ta['url']
        summary = fast_summarize(content, question)
        if summary:
            summaries.append({'url': url, 'summary': summary})
    return summaries


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api:app', host='127.0.0.1', port=8003, reload=True)