import edge_tts
import asyncio
import subprocess
import os

# 朗读人
voice = "zh-CN-XiaoxiaoNeural"
# 朗读速率
rate = "+15%"


# 子线程阅读：这里用的是 `mpv` 你也可以用其他的命令行工具
def play_thread(file_path, line_app="mpv"):
    with subprocess.Popen([
            line_app,
            file_path,
    ]) as process:
        process.communicate()
    os.remove(file_path)


# 异步文本转音频，并保存本地
async def tts_main(text, file) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(file)


# 子线程下载音频
def download_thread(text, file):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tts_main(text, file))
    loop.close()
