"""主文件"""
import asyncio
import time

from servers import get_server
from tools.cache import get_cache_mp3, rm_cache_mp3
from tools.config import get_config
from tts import download_mp3, play_mp3


async def main(chap=50):
    """主函数，两个条件只要满足一个就停止

    Args:
        chap (int, optional): 默认听100章节，自动停止. Defaults to 100.
        play_min (int, optional): 默认播放100分钟，读完当前章节自动停止. Defaults to 100.
    """
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    rm_cache_mp3()

    conf = get_config()

    lg = get_server(conf)

    txt_last = await lg.initialize()
    # 下载和播放章节
    mp3_file = f'{get_cache_mp3(f"{time.time()}")}.mp3'
    print(conf)
    await download_mp3(txt_last, mp3_file, conf)

    # 默认听100章节，自动停止
    for _i in range(chap):
        print(f"\n\n*** {_i}/{chap} ***")
        print(mp3_file)

        # 并行播放和下载任务
        task_play = play_mp3(mp3_file, conf)
        mp3_file = f'{get_cache_mp3(f"{time.time()}")}.mp3'
        task_download = download_mp3(await lg.next(), mp3_file, conf)

        await asyncio.gather(task_play, task_download)


if __name__ == "__main__":
    asyncio.run(main())
