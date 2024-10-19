"""主文件"""
import asyncio
import time

from servers import get_txts
from servers import init as init_server
from servers import play_end
from tools.cache import get_cache_mp3
from tools.config import get_config
from tts import download_mp3, play_mp3


async def play_chap(i, file_last, book_data, conf):
    """播放一个章节，分割处理

    Args:
        i (int): _description_
        book_data (dict): 书的一些数据
        conf (dict): _description_
    """
    txts, p2s, n_last = await get_txts(i, book_data, conf)

    # 根据阅读进度，跳过之前读过的（最近一章没跳过）
    for j in range(len(txts) - n_last):
        chap_n = n_last + j
        print(f"*** {j}/{len(txts)-n_last} {chap_n-1}/{len(txts)} ***")

        # 并行播放和下载任务
        task_play = play_mp3(file_last, conf)
        file_last = f"{get_cache_mp3(str(chap_n))}-{chap_n}-{len(txts)}.mp3"
        task_download = download_mp3(txts[chap_n], file_last, conf)
        task_end = play_end(p2s[chap_n], book_data, conf)

        # 等待任务完成
        await asyncio.gather(task_play, task_download, task_end)

    print("\n====最后")
    await play_mp3(file_last, conf)


async def main(chap=100, play_min=100):
    """主函数，两个条件只要满足一个就停止

    Args:
        chap (int, optional): 默认听100章节，自动停止. Defaults to 100.
        play_min (int, optional): 默认播放100分钟，读完当前章节自动停止. Defaults to 100.
    """
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    st = time.time()
    conf = get_config()
    book_data = await init_server(conf)

    # 默认听100章节，自动停止
    for i in range(chap):
        # 默认播放100分钟，一章结束再停止
        if time.time() - st > play_min * 60:
            print(f"阅读时间{(time.time() - st)/60}分钟 > {play_min}分钟")
            break

        # 下载和播放章节
        file_last = f"{get_cache_mp3(str(i))}.mp3"
        await download_mp3(book_data["chaps"][i], file_last, conf)
        await play_chap(i, file_last, book_data, conf)


async def test_play():
    """测试tts和mpv播放音频"""
    txt = "恭喜！配置成功！快打开阅读app，并修改ip地址吧！"
    file = "test.webm"
    conf = get_config()

    await download_mp3(txt, file, conf)
    await play_mp3(file, conf)


if __name__ == "__main__":
    # asyncio.run(test_play())
    asyncio.run(main())
