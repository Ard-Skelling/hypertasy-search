import sys
from pathlib import Path

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))


import aiohttp
from pydantic import BaseModel
from module.parser import Parser
from module.summary import summarize_text, get_final_answer

class WebTask(BaseModel):
    url: str

    class Config:
        extra = 'allow'

CRAWLER_URL = 'http://127.0.0.1:8002'
INDEX_URL = CRAWLER_URL + '/bing_spider/search'
DETAIL_URL = CRAWLER_URL + 'play_spider/request'
AIOHTTP_SESS = aiohttp.ClientSession()


async def john_search(query):
    params = {'q': query}
    res = await AIOHTTP_SESS.get(INDEX_URL, params=params, ssl=False)
    result = res['result']
    form = {'tasks': result}
    res = await AIOHTTP_SESS.post(DETAIL_URL, json=form)
    parser = Parser()
    summaries = []
    for ta in res:
        ta.content = parser.parse_text(ta.content)
        ta.summary = summarize_text(ta.content)
        summaries.append(ta.summary)
    res = get_final_answer(summaries, query)
    return res
    