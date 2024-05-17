"""主文件"""
import time
from threading import Thread as td

from servers import get_txts
from servers import init as init_server
from servers import play_end
from tools.cache import get_cache_mp3
from tools.config import get_config
from tts import download_mp3, play_mp3


def play_chap(i, file_last, book_data, conf):
    """播放一个章节，这里分割

    Args:
        i (int): _description_
        book_data (dict): 书的一些数据
        conf (dict): _description_
    """
    txts, p2s, n_last = get_txts(i, book_data, conf)

    # 根据阅读进度，跳过之前读过的（最近一章没跳过）
    for j in range(len(txts) - n_last):
        chap_n = n_last + j
        print(f"*** {j}/{len(txts)-n_last} {chap_n-1}/{len(txts)} ***")

        # 多线程读之前下载好的，防止卡顿、等待
        t_play = td(target=play_mp3, args=(file_last, conf))
        t_play.start()

        file_last = f"{get_cache_mp3(str(i))}-{chap_n}-{len(txts)}.mp3"
        # 多线程预下载下一段落
        t_download = td(target=download_mp3,
                        args=(txts[chap_n], file_last, conf))
        t_download.start()

        # 读了以后做什么，比如保存阅读进度
        t_end = td(target=play_end,
                    args=(p2s[chap_n], book_data, conf))
        t_end.start()

        t_play.join()
        t_download.join()
        t_end.join()

    print("\n====最后")
    # 把最后一段下载好的播放
    play_mp3(file_last, conf)



def main(chap=100, play_min=100):
    """主函数，两个条件只要满足一个就停止

    Args:
        chap (int, optional): 默认听100章节，自动停止. Defaults to 100.
        play_min (int, optional): 默认播放100分钟，读完当前章节自动停止. Defaults to 100.
    """
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    st = time.time()
    conf = get_config()
    book_data = init_server(conf)

    # 默认听100章节，自动停止
    for i in range(chap):
        # 默认播放100分钟，一章结束再停止
        if time.time() - st > play_min*60:
            print(f"阅读时间{(time.time() - st)/60}分钟 > {play_min}分钟")
            break

        # 先把这个章节的目录读一下，方便预下载下一段
        file_last = f"{get_cache_mp3(str(i))}.mp3"
        download_mp3(book_data["chaps"][i], file_last, conf)
        play_chap(i, file_last, book_data, conf)



def test_play():
    """测试tts和mpv播放音频
    """
    txt = "恭喜！配置成功！快打开阅读app，并修改ip地址吧！"
    file = "test.webm"
    conf = get_config()

    download_mp3(txt, file, conf)
    play_mp3(file, conf)


# test_play()
main()
