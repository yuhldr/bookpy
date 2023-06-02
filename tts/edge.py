"""文本转语音文件"""

import asyncio
import os
import subprocess

import edge_tts

from tts import get_config_tts


def play_mp3(file_path, line_app="mpv"):
    """子线程阅读

    Args:
        file_path (_type_): 音频文件路径
        line_app (str, optional): 这里用的是 `mpv` 你也可以用其他的命令行工具. Defaults to "mpv".
    """
    with subprocess.Popen([
            line_app,
            file_path,
    ]) as process:
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
