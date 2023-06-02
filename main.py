"""主文件"""
import threading

from servers import legado as lg
from tools import split_text
from tools.cache import get_cache_mp3, get_legado, save_legado
from tools.config import get_config
from tts.edge import download_mp3, play_mp3


def save_jd(book_data):
    """保存进度，本地也保存一下，方便不动手机，通过force强制修改阅读位置

    Args:
        book_data (dict): 请求书架获得的书籍信息
    """
    lg.save_book_progress(book_data)
    save_legado(book_data)


def init(book_n):
    """初始化：创建文件夹、获取书籍信息

    Args:
        book_n (int): 书架的第几本书

    Returns:
        dict: 请求书架获得的书籍信息
    """

    config = get_config()

    if "force" in config and config["force"]:
        return get_legado()

    return lg.get_book_shelf(book_n)


def read_chap(book_data, dcp, path):
    """读某一章节

    Args:
        book_data (dict): 书籍信息
        dcp (int): 上次读到哪里了
        path (str): 音频缓存保存位置
    """
    # 先把这个章节的目录读一下，方便预下载下一段
    file_last = f"{path}.mp3"
    download_mp3(book_data[lg.CHAP_TITLE], file_last)

    # 把这一章节分割一下，防止有些段落太短，浪费
    # ts，分割以后的文本数组
    # p2s，分割以后的每一段是第几个字符，方便保存阅读进度
    # n，之前读到第几个分割点了
    book_txt = lg.get_book_txt(book_data)
    txt_list, p2s, n_last = split_text(book_txt, dcp)

    print(f"上次：{n_last}/{len(txt_list)}\n\n")
    print(f"{dcp}/{p2s[-1]}  ts={len(txt_list)} ps={len(p2s)}")

    # 根据阅读进度，跳过之前读过的（最近一章没跳过）
    for j in range(len(txt_list) - n_last):
        n_chap = n_last + j
        print("\n\n************\n")
        print(f"{j}/{len(txt_list) - n_last} {n_chap - 1}/{len(txt_list)}")

        # 保存阅读进度
        book_data[lg.CHAP_POS] = p2s[n_chap]
        save_jd(book_data)

        # 多线程读之前下载好的，防止卡顿、等待
        play_t = threading.Thread(target=play_mp3, args=(file_last, ))
        play_t.start()
        file_last = f"{path}-{n_chap}({len(txt_list)}).mp3"

        # 多线程预下载下一段落
        download_t = threading.Thread(target=download_mp3,
                                      args=(txt_list[n_chap], file_last))
        download_t.start()

        play_t.join()
        download_t.join()

    print("\n====最后")
    # 把最后一段下载好的播放
    play_mp3(file_last)


def main(book_n=0, chap=100):
    """主函数

    Args:
        book_n (int, optional): 获取书架第0本书的信息. Defaults to 0.
        chap (int, optional): 默认听100章节，自动停止. Defaults to 100.
    """
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    book_data = init(book_n)
    # 获取书的目录
    chaps = lg.get_chapter_list(book_data)

    # 默认听100章节，自动停止
    for i in range(chap):

        dcp = 0
        if i == 0:
            dcp = book_data[lg.CHAP_POS]
        else:
            book_data[lg.CHAP_INDEX] += 1

        book_data[lg.CHAP_TITLE] = chaps[book_data[lg.CHAP_INDEX]]["title"]
        print(f"========= {book_data[lg.CHAP_TITLE]} ======")

        path = get_cache_mp3(str(book_data[lg.CHAP_INDEX]))
        read_chap(book_data, dcp, path)


def test_play():
    """测试tts和mpv播放音频
    """
    txt = "恭喜！配置成功！快打开阅读app，并修改ip地址吧！"
    file = "test.webm"
    download_mp3(txt, file)
    play_mp3(file)


# test_play()
main()
