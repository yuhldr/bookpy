"""一些工具"""
import asyncio
import copy
import os

from tts.edge import download_audio as edge_download
from tts.ms_azure import download_audio as azure_download


def get_tts_ds(conf: dict):
    """下载相关配置

    Args:
        conf (dict): 所配置

    Returns:
        _type_: _description_
    """
    return conf["tts"]["download"]


def get_td(conf):
    """获取当前选择的下载服务

    Args:
        conf (dict): 完整配置

    Returns:
        _type_: _description_
    """
    ds = get_tts_ds(conf)
    # 类似如下
    # "azure": {
    #     "key": "xxxxxxxxxxxxxx",
    #     "region": "japanwest",
    #     "language": "zh-CN",
    #     "voice": "zh-CN-XiaoxiaoNeural",
    #     "rate": "+30%"
    # }
    return ds[ds["key"]]


async def download_mp3(text, file, conf: dict):
    """下载视频

    Args:
        text (str): 文字
        file (str): 下载到哪里
        cfg (dict): 只要conf["tts"]["download"]的部分

    Returns:
        _type_: _description_
    """
    if len(text) > 20:
        print(f"{text[:20]} ...")
    else:
        print(text[:20])
    if get_tts_ds(conf)["key"] == "azure":
        await azure_download(text, file, get_td(conf))
    else:
        await edge_download(text, file, get_td(conf))


async def play_mp3(file_path, conf: dict):
    """子线程阅读

    Args:
        file_path (_type_): 音频文件路径
    """

    codes = copy.copy(conf["tts"]["play"]["code"])
    codes.append(file_path)

    process = await asyncio.create_subprocess_exec(*codes)
    await process.communicate()
    os.remove(file_path)
