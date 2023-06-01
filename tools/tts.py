"""文本转语音文件"""

import asyncio
import os
import subprocess

import edge_tts


def play_thread(file_path, line_app="mpv"):
    """子线程阅读

    Args:
        file_path (_type_): _description_
        line_app (str, optional): 这里用的是 `mpv` 你也可以用其他的命令行工具. Defaults to "mpv".
    """
    with subprocess.Popen([
            line_app,
            file_path,
    ]) as process:
        process.communicate()
    os.remove(file_path)


async def tts_main(text,
                   file,
                   voice="zh-CN-XiaoxiaoNeural",
                   rate="+15%") -> None:
    """异步文本转音频，并保存本地

    Args:
        text (_type_): _description_
        file (_type_): _description_
        voice (str, optional): 朗读人. Defaults to "zh-CN-XiaoxiaoNeural".
        rate (str, optional): 朗读速率. Defaults to "+15%".
    """
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(file)


def download_thread(text, file):
    """子线程下载音频

    Args:
        text (_type_): 文本
        file (_type_): 保存音频文件
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tts_main(text, file))
    loop.close()
