"""阅读app 相关的webapi"""

import datetime
import json
import time
import urllib

import requests

# https://github.com/gedoor/legado
# 阅读app ip和端口
HOST_BOOK = "http://192.168.31.5:1122"


def get_book_shelf(book_n=0):
    """获取书架

    Args:
        n (int, optional): _description_. Defaults to 0.

    Returns:
        dict: 书籍信息
    """
    url = HOST_BOOK + '/getBookshelf'
    print(url)
    response = requests.get(url, timeout=10)
    print(response)
    # 第几本数，建议不要动，就第一本书就行，
    # 想读某一本书的话，手机上点一下那本书
    return response.json()["data"][book_n]


def data2url(book_data):
    """_summary_

    Args:
        book_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return urllib.parse.quote(book_data["bookUrl"])


def get_book_txt(book_data):
    """获取书某一章节的文本

    Args:
        book_data (_type_): _description_
        index (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    url = f"{HOST_BOOK}/getBookContent"
    params = f"url={data2url(book_data)}&index={book_data['durChapterIndex']}"

    response = requests.get(f"{url}?{params}", timeout=10)

    return response.json()["data"]


def get_chapter_list(book_data):
    """获取书章节目录

    Args:
        book_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    url = f"{HOST_BOOK}/getChapterList?url={data2url(book_data)}"
    response = requests.get(url, timeout=10)
    return response.json()["data"]


def save_book_progress(book_data):
    """保存读取进度

    Args:
        book_data (_type_): _description_

    Raises:
        Exception: _description_
    """
    dct = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    data = {
        "name": book_data["name"],
        "author": book_data["author"],
        "durChapterIndex": book_data["durChapterIndex"],
        "durChapterPos": book_data["durChapterPos"],
        "durChapterTime": dct,
        "durChapterTitle": book_data["durChapterTitle"],
    }

    # 将数据转换为 JSON 格式
    json_data = json.dumps(data)

    # 设置请求头中的 Content-Type 为 application/json
    headers = {'Content-Type': 'application/json'}
    response = requests.post(HOST_BOOK + "/saveBookProgress",
                             data=json_data,
                             headers=headers, timeout=10).json()
    if response["isSuccess"]:
        print(f"章节：{data['durChapterIndex']}  同步读取进度：{data['durChapterPos']}")
    else:
        raise ValueError("进度保存错误！" + response["errorMsg"])
