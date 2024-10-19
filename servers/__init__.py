'''配置'''
import copy

from servers import legado as lg
from tools import split_text
from tools.cache import get_play_end, rm_cache_mp3, save_play_end

SERVER_LEGADO = "legado"


def get_conf_servers(conf: dict):
    """通过阅读，或者txt

    Returns:
        dict: 完整配置
    """
    return copy.copy(conf["server"])


def get_key(conf_server: dict):
    """通过阅读，或者txt

    Returns:
        _type_: _description_
    """
    return conf_server["key"]


def get_server(conf: dict):
    """获取当先选择的服务

    Args:
        conf (dict): 完整配置

    Returns:
        _type_: _description_
    """
    conf_servers = get_conf_servers(conf)
    return conf_servers[get_key(conf_servers)]


async def init(conf: dict):
    """初始化：创建文件夹、获取书籍信息

    Args:
        book_n (int): 书架的第几本书

    Returns:
        dict: 请求书架获得的书籍信息，必须包含["chaps"]
    """
    rm_cache_mp3()

    key = get_key(get_conf_servers(conf))
    server = get_server(conf)

    if "force" in conf and conf["force"]:
        return get_play_end(SERVER_LEGADO)

    book_data = {"chaps": [""]*100}

    if key == SERVER_LEGADO:

        book_data = await lg.get_book_shelf(0, server)
        cl = await lg.get_chapter_list(book_data, server)

        # 只要之后的章节名字
        book_data["chaps"] = cl[book_data["durChapterIndex"]:]

    return book_data


async def play_end(pos, data, conf: dict):
    """每次读完需要做什么

    Args:
        pos (_type_): p2s（每个字符在这个章节的索引位置）
        data (_type_): 当前📖相关数据
        conf (dict): 完整配置

    Returns:
        _type_: _description_
    """

    key = get_key(get_conf_servers(conf))
    server = get_server(conf)

    if key == SERVER_LEGADO:
        data[lg.CHAP_POS] = pos
        lg.save_book_progress(data, server)
        save_play_end(data, SERVER_LEGADO)


async def get_txts(i: int, data: dict, conf: dict):
    """返回待朗读的文本

    Args:
        i (int): _description_
        data (dict): _description_
        conf (dict): _description_

    Returns:
        _type_: 把这一章节分割一下，防止有些段落太短，浪费
        list[str]: ts，分割以后的文本数组
        list[int] p2s，分割以后的每一段是第几个字符，方便保存阅读进度
        int n，之前读到第几个分割点了
    """
    txts = []

    key = get_key(get_conf_servers(conf))
    server = get_server(conf)

    if key == SERVER_LEGADO:

        if i != 0:
            data[lg.CHAP_INDEX] += 1
            data[lg.CHAP_POS] = 0

        book_txt = await lg.get_book_txt(data, server)
        txts, p2s, n_last = split_text(book_txt, data[lg.CHAP_POS])

        return txts, p2s, n_last

    return txts, 0, 0
