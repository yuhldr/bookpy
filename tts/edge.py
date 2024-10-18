"""文本转语音文件"""

import asyncio

import edge_tts


async def tts_main(text, file, conf) -> None:
    """异步文本转音频，并保存本地

    Args:
        text (str): 文本
        file (str): 保存的音频文件
        conf (dict): 配置 conf["tts"]["download"]["edge"]. 

    """
    communicate = edge_tts.Communicate(text, conf["voice"], rate=conf["rate"])
    await communicate.save(file)


def download_audio(text, file, conf):
    """子线程下载音频

    Args:
        text (str): 文本
        file (str): 保存的音频文件
        conf (dict): 配置 conf["tts"]["download"]["edge"]. 
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tts_main(text, file, conf))
    loop.close()
