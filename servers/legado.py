"""阅读app 相关的webapi"""

import datetime
import json
import time
import urllib

import requests

# https://github.com/gedoor/legado

# 当前阅读位置：第几个字符
CHAP_POS = "durChapterPos"
# 当前第几章节
CHAP_INDEX = "durChapterIndex"
# 当前章节题目
CHAP_TITLE = "durChapterTitle"


def get_base_url(conf_legado: dict):
    """设置ip

    Args:
        conf_legado (dict): 配置 conf["legado"]. 


    Returns:
        _type_: _description_
    """
    return f'http://{conf_legado["ip"]}:{conf_legado["port"]}'


def get_book_shelf(book_n, conf: dict):
    """获取书架

    Args:
        n (int): 第几本书. 
        conf (dict): 配置 conf["legado"]. 

    Returns:
        dict: 书籍信息
    """
    url = get_base_url(conf) + '/getBookshelf'
    print(url)
    response = requests.get(url, timeout=10)
    # 第几本数，建议不要动，就第一本书就行，
    # 想读某一本书的话，手机上点一下那本书
    return response.json()["data"][book_n]


def data2url(book_data):
    """这个url需要编码才行

    Args:
        book_data (dict): 书籍信息

    Returns:
        str: 编码以后的图书信息url
    """
    return urllib.parse.quote(book_data["bookUrl"])


def get_book_txt(book_data, conf):
    """获取书某一章节的文本

    Args:
        book_data (dict): 书籍信息
        conf (dict): 配置 conf["legado"]. 

    Returns:
        str: 某一章节的文字
    """
    url = f"{get_base_url(conf)}/getBookContent"
    # 因为data2url需要编码的问题，不能写成字典
    params = f"url={data2url(book_data)}&index={book_data[CHAP_INDEX]}"

    response = requests.get(f"{url}?{params}", timeout=10)

    return response.json()["data"]


def get_chapter_list(book_data: dict, conf: dict):
    """获取书章节目录

    Args:
        book_data (dict): 书籍信息
        conf (dict): 配置 conf["legado"]. 

    Returns:
        list: 目录json，包含title,url等等
    """
    url = f"{get_base_url(conf)}/getChapterList?url={data2url(book_data)}"
    response = requests.get(url, timeout=10)
    data = response.json()["data"]
    titles = []
    for d in data:
        titles.append(d["title"])
    return titles


def save_book_progress(book_data: dict, conf: dict):
    """保存读取进度

    Args:
        book_data (dict): 书籍信息

    Raises:
        Exception: _description_
    """
    dct = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    data = {
        "name": book_data["name"],
        "author": book_data["author"],
        CHAP_INDEX: book_data[CHAP_INDEX],
        CHAP_POS: book_data[CHAP_POS],
        "durChapterTime": dct,
        CHAP_TITLE: book_data[CHAP_TITLE],
    }

    # 将数据转换为 JSON 格式
    json_data = json.dumps(data)

    # 设置请求头中的 Content-Type 为 application/json
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{get_base_url(conf)}/saveBookProgress",
                             data=json_data,
                             headers=headers, timeout=10)

    if not response.json()["isSuccess"]:
        raise ValueError(f'进度保存错误！\n{response.json()["errorMsg"]}')

    print(f"{data[CHAP_INDEX]}：{data[CHAP_POS]}")
