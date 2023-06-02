"""文本转语音文件"""

import asyncio
import os
import subprocess

import edge_tts

from tts import get_config_tts


def play_mp3(file_path):
    """子线程阅读

    Args:
        file_path (_type_): 音频文件路径
    """
    cfg = get_config_tts()["play"]["code"]
    cfg.append(file_path)

    with subprocess.Popen(cfg) as process:
        process.communicate()
    os.remove(file_path)


async def tts_main(text,
                   file) -> None:
    """异步文本转音频，并保存本地

    Args:
        text (_type_): 文本
        file (_type_): 保存的音频文件
    """
    cfg = get_config_tts()["edge"]
    communicate = edge_tts.Communicate(text, cfg["voice"], rate=cfg["rate"])
    await communicate.save(file)


def download_mp3(text, file):
    """子线程下载音频

    Args:
        text (_type_): 文本
        file (_type_): 保存的音频文件
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tts_main(text, file))
    loop.close()
