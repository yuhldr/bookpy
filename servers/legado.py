"""阅读app 相关的webapi"""

import datetime
import json
import time
import urllib

import aiohttp

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


async def get_book_shelf(book_n, conf: dict):
    """异步获取书架信息

    Args:
        book_n (int): 第几本书
        conf (dict): 配置 conf["legado"]. 

    Returns:
        dict: 书籍信息
    """
    url = get_base_url(conf) + '/getBookshelf'
    print(url)

    # 使用 aiohttp 进行异步 GET 请求
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            resp_json = await response.json(content_type=None)

    # 返回书架中的第 book_n 本书的信息
    return resp_json["data"][book_n]


def data2url(book_data):
    """这个url需要编码才行

    Args:
        book_data (dict): 书籍信息

    Returns:
        str: 编码以后的图书信息url
    """
    return urllib.parse.quote(book_data["bookUrl"])


async def get_book_txt(book_data, conf):
    """异步获取书某一章节的文本

    Args:
        book_data (dict): 书籍信息
        conf (dict): 配置 conf["legado"]. 

    Returns:
        str: 某一章节的文字
    """
    url = f"{get_base_url(conf)}/getBookContent"
    # 因为data2url需要编码的问题，不能写成字典
    params = f"url={data2url(book_data)}&index={book_data[CHAP_INDEX]}"

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}?{params}", timeout=10) as response:
            resp_json = await response.json(content_type=None)

    return resp_json["data"]


async def get_chapter_list(book_data: dict, conf: dict):
    """异步获取书章节目录

    Args:
        book_data (dict): 书籍信息
        conf (dict): 配置 conf["legado"]. 

    Returns:
        list: 目录json，包含title,url等等
    """
    url = f"{get_base_url(conf)}/getChapterList?url={data2url(book_data)}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            resp_json = await response.json(content_type=None)

    data = resp_json["data"]
    titles = [d["title"] for d in data]

    return titles


async def save_book_progress(book_data: dict, conf: dict):
    """异步保存读取进度

    Args:
        book_data (dict): 书籍信息

    Raises:
        Exception: 进度保存错误时抛出异常
    """
    # 当前时间戳转换为毫秒级
    dct = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)

    # 构建请求数据
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

    # 使用 aiohttp 进行异步 POST 请求
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{get_base_url(conf)}/saveBookProgress",
                                data=json_data,
                                headers=headers,
                                timeout=10) as response:
            # 异步获取响应的 JSON 数据
            resp_json = await response.json(content_type=None)

            # 判断请求是否成功
            if not resp_json["isSuccess"]:
                raise ValueError(f'进度保存错误！\n{resp_json["errorMsg"]}')

            # 打印章节进度信息
            print(f"{data[CHAP_INDEX]}：{data[CHAP_POS]}")
