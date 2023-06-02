"""阅读app 相关的webapi"""

import datetime
import json
import time
import urllib

import requests

from servers import get_config_server

# https://github.com/gedoor/legado

# 当前阅读位置：第几个字符
CHAP_POS = "durChapterPos"
# 当前第几章节
CHAP_INDEX = "durChapterIndex"
# 当前章节题目
CHAP_TITLE = "durChapterTitle"


def get_base_url():
    """设置ip

    Args:
    """
    config = get_config_server()["legado"]
    return f'http://{config["ip"]}:{config["port"]}'


def get_book_shelf(book_n=0):
    """获取书架

    Args:
        n (int, optional): 第几本书. Defaults to 0.

    Returns:
        dict: 书籍信息
    """
    url = get_base_url() + '/getBookshelf'
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


def get_book_txt(book_data):
    """获取书某一章节的文本

    Args:
        book_data (dict): 书籍信息
        index (int, optional): _description_. Defaults to 0.

    Returns:
        str: 某一章节的文字
    """
    url = f"{get_base_url()}/getBookContent"
    # 因为data2url需要编码的问题，不能写成字典
    params = f"url={data2url(book_data)}&index={book_data[CHAP_INDEX]}"

    response = requests.get(f"{url}?{params}", timeout=10)

    return response.json()["data"]


def get_chapter_list(book_data):
    """获取书章节目录

    Args:
        book_data (dict): 书籍信息

    Returns:
        list: 目录json，包含title,url等等
    """
    url = f"{get_base_url()}/getChapterList?url={data2url(book_data)}"
    response = requests.get(url, timeout=10)
    return response.json()["data"]


def save_book_progress(book_data):
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
    response = requests.post(get_base_url() + "/saveBookProgress",
                             data=json_data,
                             headers=headers, timeout=10)

    if response.json()["isSuccess"]:
        print(f"{data[CHAP_TITLE]}（{data[CHAP_INDEX]}）：{data[CHAP_POS]}")
    else:
        raise ValueError("进度保存错误！" + response.json()["errorMsg"])
