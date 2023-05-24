import sys
from pathlib import Path

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))

import requests, asyncio, re
from typing import Union, List, Dict
from fastapi import FastAPI, Request
from pydantic import BaseModel
from module.parser import Parser
from module.summary import summarize_text, get_final_answer, fast_summarize, one_one_simi, enhance_search_keywords

# TODO: authentication

class PostData(BaseModel):
    document: str = ''
    question: str = ''
    url = ''

    class Config:
        extra = 'ignore'

app = FastAPI()

class WebTask(BaseModel):
    url: str

    class Config:
        extra = 'allow'

CRAWLER_URL = 'http://127.0.0.1:8002'
NLP_URL = 'http://127.0.0.1:8001'
# NLP_URL = 'http://47.92.81.63:9527'
INDEX_URL = CRAWLER_URL + '/bing_spider/search'
SEARX_URL = 'http://54.151.16.174:8888/search'
DETAIL_URL = CRAWLER_URL + '/play_spider/request'


def get_ems(sentences):
    ...


@app.post('/john_chat/chat_url')
async def john_chat_url(post_data: PostData):
    url = post_data.url
    question = post_data.question
    task = {'url': url}
    form = {
        'tasks': task
    }
    resp = requests.post(DETAIL_URL, json=form)
    document = resp.json()[0]['content']
    parser = Parser()
    content = parser.parse_text(document)
    # summary = summarize_text(content, question)
    summary = fast_summarize(content, question)
    if not summary:
        return '无可奉告，还是另请高明吧。'
    return summary

@app.post('/john_chat/')
async def john_chat(post_data: PostData):
    document = post_data.document
    question = post_data.question
    parser = Parser()
    content = parser.parse_text(document)
    # summary = summarize_text(content, question)
    summary = fast_summarize(content, question)
    if not summary:
        return '无可奉告，还是另请高明吧。'
    return summary

@app.post('/chat_text/')
async def john_chat(post_data: PostData):
    document = post_data.document
    question = post_data.question
    # summary = summarize_text(content, question)
    summary = fast_summarize(document, question)
    if not summary:
        return '无可奉告，还是另请高明吧。'
    return summary

@app.get('/john_search/')
async def john_search(request: Request):
    query = request.query_params.get('q')
    question = request.query_params.get('question') or query
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
    # 增加最大爬虫任务上限为10
    form = {'tasks': result[:10]}
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

@app.get('/john_nb_search/')
async def john_nb_search(request: Request):
    query = request.query_params.get('q')
    question = request.query_params.get('question') or query
    search_kws = enhance_search_keywords(query)
    short_kws = []
    long_kws = []
    for kw in search_kws:
        if len(kw) <= 5:
            short_kws.append(kw)
        else:
            long_kws.append(kw)
    long_kws.append(' '.join(short_kws))
    long_kws = [kw for kw in long_kws if re.findall('[一-龥a-zA-Z]', kw)][:5]
    query = ' '.join(long_kws)
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
    # 增加最大爬虫任务上限为10
    form = {'tasks': result[:10]}
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

@app.get('/light_search/')
async def light_search(request: Request):
    query = request.query_params.get('q')
    question = request.query_params.get('question') or query
    search_kws = enhance_search_keywords(question)
    short_kws = []
    long_kws = []
    for kw in search_kws:
        if len(kw) <= 5:
            short_kws.append(kw)
        else:
            long_kws.append(kw)
    long_kws.append(' '.join(short_kws))
    long_kws = [kw for kw in long_kws if re.findall('[一-龥a-zA-Z]', kw)][:5]
    long_kws = [' '.join(long_kws)]
    final_result = []
    final_res = []
    engine = request.query_params.get('engine')
    under_engine = request.query_params.get('under_engine')
    for kw in long_kws:
        print(f'search keyword: {kw}')
        if engine == 'searx':
            params = {'q': kw, 'format': 'json', 'engine': under_engine}
            res = requests.get(SEARX_URL, params=params)
            res = res.json()
            res = res['results']
            if not res:
                return '无可奉告，还是另请高明吧。'
            result = [r.get('content') for r in res if r.get('content')]
            temp = []
            for r in res:
                temp.append({
                    'url': r.get('pretty_url', ''),
                    'snippet': r.get('content', '')
                })
            res = temp
        else:
            params = {'q': kw}
            res = requests.get(INDEX_URL, params=params)
            res = res.json()
            res = res['result']
            if not res:
                return '无可奉告，还是另请高明吧。'
            result = [r['snippet'] for r in res if r.get('snippet')]
            for r in res:
                r.pop('title')
    final_result += result
    final_res += res
    final_result = '\n'.join(final_result)
    summary = fast_summarize(final_result, question)
    if summary:
        return {'summary': summary, 'refer': final_res}
    else:
        return {'summary': '无可奉告，还是另请高明吧。', 'refer': []}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api:app', host='127.0.0.1', port=8003, reload=True)