"""主文件"""

import json
import os
import shutil
import threading

from servers.legado import (get_book_shelf, get_book_txt, get_chapter_list,
                            save_book_progress)
from tools import split_text
from tools.tts import download_thread, play_thread

# 缓存位置
# path_cache = "./"
# path_config = "./"
path_cache = os.getenv("HOME") + "/.cache/tts/"
path_config = os.getenv("HOME") + "/.config/tts/"


def save_jd(book_data):
    """保存进度，本地也保存一下，方便不动手机，通过force强制修改阅读位置

    Args:
        book_data (dict): 请求书架获得的书籍信息
    """
    save_book_progress(book_data)
    with open(path_config + "jd.json", 'w', encoding="utf-8") as file:
        json.dump(book_data,
                  file,
                  indent=4,
                  ensure_ascii=False)


def init(book_n):
    """初始化：创建文件夹、获取书籍信息

    Args:
        book_n (_type_): 书架的第几本书

    Returns:
        dict: 请求书架获得的书籍信息
    """
    if not os.path.exists(path_config):
        os.mkdir(path_config)

    if os.path.exists(path_cache):
        shutil.rmtree(path_cache)
    os.mkdir(path_cache)

    with open(path_config + "jd.json", "r", encoding="utf-8") as file:
        book_data = json.load(file)
    if "force" in book_data and book_data["force"]:
        return book_data

    return get_book_shelf(book_n)


def read_chap(book_data, dcp, path):
    """读某一章节

    Args:
        book_data (_type_): 书籍信息
        dcp (_type_): 上次读到哪里了
        path (_type_): 音频缓存保存位置
    """
    # 先把这个章节的目录读一下，方便预下载下一段
    file_last = f"{path}.mp3"
    download_thread(book_data['durChapterTitle'], file_last)

    # 把这一章节分割一下，防止有些段落太短，浪费
    # ts，分割以后的文本数组
    # p2s，分割以后的每一段是第几个字符，方便保存阅读进度
    # n，之前读到第几个分割点了
    book_txt = get_book_txt(book_data)
    txt_list, p2s, n_last = split_text(book_txt, dcp)

    print(f"========= {book_data['durChapterTitle']} ======")
    print(f"上次：{n_last}/{len(txt_list)}\n\n")
    print(f"{dcp}/{p2s[-1]}  ts={len(txt_list)} ps={len(p2s)}")

    # 根据阅读进度，跳过之前读过的（最近一章没跳过）
    for j in range(len(txt_list) - n_last):
        n_chap = n_last + j
        print("\n\n************\n")
        print(f"{j}/{len(txt_list) - n_last} {n_chap - 1}/{len(txt_list)}")

        # 保存阅读进度
        book_data["durChapterPos"] = p2s[n_chap]
        save_jd(book_data)

        # 多线程读之前下载好的，防止卡顿、等待
        play_t = threading.Thread(target=play_thread, args=(file_last, ))
        play_t.start()
        file_last = f"{path}-{n_chap}({len(txt_list)}).mp3"

        # 多线程预下载下一段落
        download_t = threading.Thread(target=download_thread,
                                      args=(txt_list[n_chap], file_last))
        download_t.start()

        play_t.join()
        download_t.join()

    print("\n====最后")
    # 把最后一段下载好的播放
    play_thread(file_last)


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
    chapter_list = get_chapter_list(book_data)

    # 默认听100章节，自动停止
    for i in range(chap):
        dur_chap_i = book_data["durChapterIndex"] + 1
        book_data["durChapterIndex"] = dur_chap_i
        book_data["durChapterTitle"] = chapter_list[dur_chap_i]["title"]

        dcp = 0
        if i == 0:
            dcp = book_data["durChapterPos"]
            print(dcp)

        path = f"{path_cache}{dur_chap_i}"

        read_chap(book_data, dcp, path)


def test_play():
    """测试tts和mpv播放音频
    """
    txt = "恭喜！配置成功！快打开阅读app，并修改ip地址吧！"
    file = "test.webm"
    download_thread(txt, file)
    play_thread(file)


# test_play()
main()
