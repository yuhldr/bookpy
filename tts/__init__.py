"""一些工具"""
import asyncio
import copy
import os

from tts.edge import download_audio as edge_download
from tts.ms_azure import download_audio as azure_download


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

    conf_ttss = conf["tts"]["download"]
    conf_tts_key = conf_ttss["key"]
    conf_tts = conf_ttss[conf_tts_key]

    if conf_tts_key == "azure":
        await azure_download(text, file, conf_tts)
    else:
        await edge_download(text, file, conf_tts)


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
