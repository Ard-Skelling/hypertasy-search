import os
import re
import heapq
import pymongo
import aiohttp
import uvicorn
import torch
from datetime import datetime
from typing import Union
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel, validator
from spider.search_engine_spider import BingSpider
from lxml import etree
from bs4 import BeautifulSoup


from InstructorEmbedding import INSTRUCTOR
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = INSTRUCTOR('hkunlp/instructor-large', cache_folder=r'G:\nlp_models')

CLIENT = pymongo.MongoClient(os.getenv('MONGODB_CONN_STR'))
# CLIENT = pymongo.MongoClient('mongodb://John:Cyber_2077@localhost:27017/')
COLL = CLIENT.ai_search.bing
TODAY_STR = datetime.today().strftime('%Y-%m-%d')

app = FastAPI()


class TextRegu(BaseModel):
    text: str

    @validator('text')
    def format_text(cls, v):
        ...


class Instructor:
    def __init__(self):
        ...

    @staticmethod
    def parse(html):
        # html = etree.HTML(html)
        # texts = html.xpath("//p//text()")
        # s_texts = [t.strip() for t in texts if re.sub('\s', '', t)]
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text()
        text = re.sub('\n+|\r+|\t+', '\n', text).strip()
        text = text.split('\n')
        s_text = []
        for t in text:
            st = re.sub(' +', ' ', t).strip()
            if st:
                s_text.append(st)
        combined = []
        for i in range(len(s_text) - 4):
            text = '\n'.join(s_text[i:i + 5])
            combined.append(text)
        return combined

    @staticmethod
    def construct_corpus(texts, text_type, type_objective='', domain=''):
        res = []
        instructor = 'Represent'
        if domain:
            instructor += ' ' + domain + ' '
        instructor += text_type
        if type_objective:
            instructor += ' for ' + type_objective
        instructor += ': '
        if isinstance(texts, str):
            texts = [texts]
        for text in texts:
            res.append([instructor, text])
        return res

    def calculate_top_n(self, query, corpus, query_type, corpus_type, query_objective='', corpus_objective='', domain='', n=20):
        query_ins = self.construct_corpus(query, query_type, query_objective, domain)
        corpus_ins = self.construct_corpus(corpus, corpus_type, corpus_objective, domain)
        query_embeddings = model.encode(query_ins)
        corpus_embeddings = model.encode(corpus_ins)
        similarities = cosine_similarity(query_embeddings, corpus_embeddings)
        simi = similarities.tolist()[0]
        top_n = heapq.nlargest(n, enumerate(simi), key=lambda x: x[1])
        return top_n

    @staticmethod
    def construct_prompts(query, top5, texts):
        prompt = f'''You are asked "{query}", retrieving answer from following documents and your real world knowledge. Return in format "My answer: blablabla"\n'''
        infos = ''
        for cit, (ind, score) in enumerate(top5):
            text = texts[ind]
            infos = infos + '\n' + f'{cit + 1}.' + text
        prompt += infos
        return prompt, infos





class Sentences(BaseModel):
    sentences: Union[str, list]

# @app.get('/encode/{sents}')
# async def encode(sents):
#     return MODEL.encode(sents).tolist()

@app.get('/search/')
async def search(q):
    tasks = []
    res = COLL.count_documents({'query': q, 'date': TODAY_STR}, limit=1)
    if not res:
        spider = BingSpider()
        _ = await spider.api_search(q)
    cursor = COLL.find({'query': q, 'date': TODAY_STR})
    for rec in cursor:
        tasks.append(rec)
    prompt, infos = calculate(q, tasks)
    infos = infos.strip()
    infos = infos.split('\n')[0]
    infos = re.sub('1\. ', '', infos)
    return infos

@app.get('/search_many/')
async def search(q):
    tasks = []
    res = COLL.count_documents({'query': q, 'date': TODAY_STR}, limit=1)
    if not res:
        spider = BingSpider()
        _ = await spider.api_search(q)
    cursor = COLL.find({'query': q, 'date': TODAY_STR})
    for rec in cursor:
        tasks.append(rec)
    prompt, infos = calculate(q, tasks)
    infos = infos.strip()
    return infos

@app.get('/enhance_search/')
async def search(q):
    tasks = []
    res = COLL.count_documents({'query': q, 'date': TODAY_STR}, limit=1)
    if not res:
        spider = BingSpider()
        _ = await spider.api_search(q)
    cursor = COLL.find({'query': q, 'date': TODAY_STR})
    for rec in cursor:
        tasks.append(rec)
    prompt, infos = calculate(q, tasks)
    headers = {'x-api-key': os.getenv('OPENAI_KEY')}
    form = {'prompt': prompt}
    async with aiohttp.ClientSession() as sess:
        async with sess.post('http://54.251.70.172:80/completion/', data=form, headers=headers) as resp:
            text = await resp.text()
    return text

def calculate(query, tasks):
    instructor = Instructor()
    ids = []
    corpus = []
    for rec in tasks:
        ids.append(rec['url'])
        corpus.append(rec['snippet'])
        html = rec.get('text')
        try:
            combined = instructor.parse(html)
        except Exception as e:
            print(e)
            print(rec['url'])
            continue
        for cor in combined:
            ids.append(rec['url'])
            corpus.append(cor)
    top_n = instructor.calculate_top_n(query, corpus, query_type='question', corpus_type='document', query_objective='retrieving supporting documents', corpus_objective='retrieval', domain='Business')
    prompt, infos = instructor.construct_prompts(query, top_n, corpus)
    return prompt, infos



if __name__ == '__main__':
    uvicorn.run('nlp_model:app', host='127.0.0.1', port=8000, reload=True)
    ...
