"""文本转语音文件"""

import edge_tts


async def download_audio(text, file, conf):
    """异步文本转音频，并保存本地

    Args:
        text (str): 文本
        file (str): 保存的音频文件
        conf (dict): 配置 conf["tts"]["download"]["edge"]. 

    """
    communicate = edge_tts.Communicate(text, conf["voice"], rate=conf["rate"])
    await communicate.save(file)
