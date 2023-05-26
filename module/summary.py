<<<<<<< HEAD
import sys
from pathlib import Path
import requests, re, json
=======
import requests, re, json, openai
>>>>>>> main
import torch
import torch.nn.functional as F
from pydantic import BaseModel
import json

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))

<<<<<<< HEAD
from data_storage import RedisClient

ChatGLM_API = 'http://39.104.82.158:8001'
ChatGLM_API = 'http://47.92.115.31:9527'
=======
# ChatGLM_API = 'http://127.0.0.1:8001'
ChatGLM_API = 'http://39.98.249.110:9527'
>>>>>>> main
EMBEDDING_API = ChatGLM_API + '/tbc_embedding'

openai.api_key = "EMPTY" # Not support yet
openai.api_base = "http://39.98.249.110:9528/v1"

VICUNA_MODEL = "vicuna-13b-v1.1"

# create a completion
def vicuna_completion(prompt):
    (k, v), = prompt.items()
    completion = openai.Completion.create(model=VICUNA_MODEL, prompt=v, max_tokens=2048)
    return completion.choices[0].text

# create a chat completion
def vicuna_chat_completion(prompt):
    (k, v), = prompt.items()
    completion = openai.ChatCompletion.create(
        model=VICUNA_MODEL,
        messages=[{"role": "user", "content": v}]
    )
    return completion.choices[0].message.content


class Summary(BaseModel):
    ...


class ChatGLMSummary(Summary):
    ...

    async def summarize_text(self, text, question):
        ...

def fast_summarize(text, question, c_ems_md5 = ""):
    if not text:
        return '无可奉告，还是另请高明吧。'
    chunks = list(split_text_overlapping(text, max_length=400, overlapping=20))

    chunks, scores = get_top_n(chunks, question, 5, c_ems_md5=c_ems_md5)

    collection = []
    for chunk, score in zip(chunks, scores):
        if score >= 0.3:
            collection.append(chunk)
            
    chunks = '\n'.join(collection)

    if not chunks:
        return '无可奉告，还是另请高明吧。'
    if len(chunks) > 2048:
        return summarize_text(chunks, question)
    prompt = create_message(chunks, question)
    r = requests.post(ChatGLM_API, json=prompt)
    summary = r.json()['response']
<<<<<<< HEAD

    if not summary:
        return '无可奉告，还是另请高明吧。'
    
=======
    # summary = vicuna_chat_completion(prompt)
>>>>>>> main
    return summary

def answer_filter(prompt, summary):
    p_chunks = list(split_text_overlapping(prompt, max_length=300, overlapping=30))
    max_score = 0.
    for p in p_chunks:
        simi = one_one_simi(p, summary)
        if simi > max_score:
            max_score = simi
    if max_score > 0.3:
        return True
    else:
        False


def get_top_n(chunks, question, n, c_ems_md5:str = ""):
    n = min(len(chunks), n)
    form = {
        'prompt': ''
    }
<<<<<<< HEAD

    # redis
    if c_ems_md5 and (c_ems_string := RedisClient().conn.get(c_ems_md5)):
        c_ems_list = json.loads(c_ems_string)
        c_ems = torch.tensor(c_ems_list)
    else:
        form.update({'prompt': chunks})
        res = requests.post(EMBEDDING_API, json=form)
        res = res.json()
        c_ems = torch.tensor(res)
        c_ems = F.normalize(c_ems)

        # 使用redis进行简单的存储，后面还是向量数据库存储向量好一点
        c_ems_string = str(c_ems.tolist())
        RedisClient().conn.set(c_ems_md5, c_ems_string, ex=600)

    form.update({'prompt': question})
=======
    form.update({'prompt': chunks})
    res = requests.post(EMBEDDING_API, json=form)
    res = res.json()
    c_ems = torch.tensor(res)
    c_ems = F.normalize(c_ems)
    form.update({'prompt': [question]})
>>>>>>> main
    res = requests.post(EMBEDDING_API, json=form)
    res = res.json()
    q_em = torch.tensor(res)
    q_em = F.normalize(q_em)
    simi = torch.cosine_similarity(q_em, c_ems)
    top_n = torch.topk(simi, n)
    return [chunks[i] for i in top_n.indices], top_n.values.tolist()

def cos_cluster(chunks, n):
    form = {
        'prompt': ''
    }
    form.update({'prompt': chunks})
    res = requests.post(EMBEDDING_API, json=form)
    res = res.json()
    ems = torch.tensor(res)
    ems = F.normalize(ems)
    simi = torch.cosine_similarity(ems, ems)
    top_n = torch.topk(simi, n)
    return [chunks[i] for i in top_n.indices], top_n.values.tolist()

def one_one_simi(content, question):
    form = {
        'prompt': ''
    }
    form.update({'prompt': content})
    res = requests.post(EMBEDDING_API, json=form)
    res = res.json()
    c_ems = torch.tensor(res)
    c_ems = F.normalize(c_ems)
    form.update({'prompt': question})
    res = requests.post(EMBEDDING_API, json=form)
    res = res.json()
    q_em = torch.tensor(res)
    q_em = F.normalize(q_em)
    simi = torch.cosine_similarity(q_em, c_ems)
    simi = simi.item()
    return simi


def get_final_answer(summary_list, question):
    prompt = create_prompt(summary_list, question)
    r = requests.post(ChatGLM_API, json=prompt)
    summary = r.json()['response']
    # summary = vicuna_chat_completion(prompt)
    return summary

def summarize_text(text, question):
    if not text:
        return "Error: No text to summarize"

    text_length = len(text)
    print(f"Text length: {text_length} characters")

    summaries = []
    chunks = list(split_text_overlapping(text))

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i + 1} / {len(chunks)}")
        prompt = create_message(chunk, question)

        # summary = create_chat_completion(
        #     model="gpt-3.5-turbo",
        #     messages=messages,
        #     max_tokens=300,
        # )
        r = requests.post(ChatGLM_API, json=prompt)
        summary = r.json()['response']
        # summary = vicuna_chat_completion(prompt)
        summaries.append(summary)

    print(f"Summarized {len(chunks)} chunks.")

    combined_summary = "\n".join(summaries)
    prompt = create_message(combined_summary, question)

    r = requests.post(ChatGLM_API, json=prompt)
    summary = r.json()['response']
    # summary = vicuna_chat_completion(prompt)
    return summary

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

def split_text_overlapping(text, max_length=1024, overlapping=200):
    text = re.sub('\n+|\r+|\t+', '\n', text)
    text = re.sub(' +', ' ', text).strip()
    toal_len = len(text)
    pre_start = 0
    pre_stop = max_length
    while True:
        chunk = text[pre_start:pre_stop]
        yield chunk
        pre_start += max_length - overlapping
        pre_stop += max_length - overlapping
        if pre_stop >= toal_len:
            break
    yield chunk



def create_message(chunk, question):
    return {
        "prompt": f'"""# 内容开始\n{chunk}\n# 内容结束"""\n根据上述内容，一步步推理，回答下面的问题: "{question}"\n--以"回答：xxx"的格式返回结果。答案尽量精确，如果没有答案，寻找最有可能的答案，返回"推测最有可能的答案是：" + 可能的回答'
    }

# def create_message(chunk, question):
#     return {
#         "prompt": f'"""# 内容开始\n{chunk}\n# 内容结束"""\n根据上述内容和你的知识, 回答下面的问题: "{question}" -- 以"回答：xxx。依据：xxx"的格式返回结果'
#     }

def create_prompt(summary_list, question):
    prompt = '# 内容开始\n'
    for i, summary in enumerate(summary_list):
        prompt += f'{i}. {summary}\n'
    prompt += f'# 内容结束\n根据上述内容和你的领域知识, 回答下面的问题: "{question}" -- 如果没有答案，返回"无可奉告，还是另请高明吧。"。以“回答：xxx。依据：xxx”的格式返回'
    return {'prompt': prompt}


# def scroll_to_percentage(driver, ratio):
#     if ratio < 0 or ratio > 1:
#         raise ValueError("Percentage should be between 0 and 1")
#     driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {ratio});")

def enhance_search_keywords(question):
    prompt = f'''
        你是约翰小助手。你收到了如下问题：
        {question}
        将问题分解为一个或多个用于在搜索引擎中进行搜索关键词。以“[关键词1, 关键词2, 关键词3]”的JSON形式返回用于搜索的关键词。回答尽量简洁。
    '''
    form = {'prompt': prompt}
    r = requests.post(ChatGLM_API, json=form)
    keywords = r.json()['response']
    # keywords = vicuna_chat_completion(form)
    keywords = re.findall('\[.*?\]', keywords, re.S)
    if not keywords:
        return [question]
    all_kws = []
    for kw_group in keywords:
        kws = re.sub('"|“|”', '', kw_group)
        kws = re.split(',|，', kws, re.S)
        all_kws += kws
    keywords = [k.strip() for k in all_kws]
    # keywords = [kw.strip() for kw in keywords.split('|')]
    # keywords = json.loads(keywords)
    return keywords


if __name__ == '__main__':
    chunks = [
        '地瓜味道很好！',
        '我是一只小黄鸡',
        '樱桃小丸子的爷爷参加抗日游击队。'
    ]
    question = '今天晚上吃啥？'
    res = one_one_simi(chunks[2], question)
    print(res)