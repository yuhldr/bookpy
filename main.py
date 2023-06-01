import threading
import os
import shutil
import json
from servers.legado import get_book_shelf, get_book_txt
from servers.legado import getChapterList, saveBookProgress
from tools.tts import play_thread, download_thread
from tools import split_text

# 缓存位置
path_cache = "./"
path_config = "./"

try:
    path_cache = os.getenv("HOME") + "/.cache/tts/"
    path_config = os.getenv("HOME") + "/.config/tts/"
except Exception as e:
    print(e)


# 保存进度，本地也保存一下，方便不动手机，通过force强制修改阅读位置
def save_jd(book_data):
    saveBookProgress(book_data)
    json.dump(book_data,
              open(path_config + "jd.json", 'w'),
              indent=4,
              ensure_ascii=False)


def init(book_n):
    if not os.path.exists(path_config):
        os.mkdir(path_config)

    if os.path.exists(path_cache):
        shutil.rmtree(path_cache)
    os.mkdir(path_cache)

    try:
        book_data = json.load(open(path_config + "jd.json", "r"))
        if "force" in book_data and book_data["force"]:
            return book_data
    except Exception as e:
        print(e)

    return get_book_shelf(book_n)


def main(
    book_n=0,
    chap=100,
):
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    book_data = init(book_n)
    # 获取书的目录
    cs = getChapterList(book_data)

    # 默认听100章节，自动停止
    for i in range(chap):
        ci = book_data["durChapterIndex"] + i
        title = cs[ci]["title"]
        book_txt = get_book_txt(book_data, ci)
        book_data["durChapterIndex"] = ci

        dcp = 0
        if i == 0:
            dcp = book_data["durChapterPos"]
            print(dcp)

        # 把这一章节分割一下，防止有些段落太短，浪费
        # ts，分割以后的文本数组
        # p2s，分割以后的每一段是第几个字符，方便保存阅读进度
        # n，之前读到第几个分割点了
        ts, p2s, n = split_text(book_txt, dcp)

        print("===============\n\n%s\n第%d个 | %d/%d  ts=%d ps=%d" %
              (title, n, dcp, p2s[-1], len(ts), len(p2s)))

        path = "%s%d" % (path_cache, ci)

        # 先把这个章节的目录读一下，方便预下载下一段
        file_last = "%s.mp3" % (path)
        download_thread(title, file_last)

        # 根据阅读进度，跳过之前读过的（最近一章没跳过）
        for j in range(len(ts) - n):
            jj = n + j
            print("\n\n************\n%d/%d  %d/%d" % (
                j,
                len(ts) - n,
                jj - 1,
                len(ts),
            ))

            # 保存阅读进度
            book_data["durChapterPos"] = p2s[jj]
            save_jd(book_data)

            # 多线程读之前下载好的，防止卡顿、等待
            play_t = threading.Thread(target=play_thread, args=(file_last, ))
            play_t.start()
            file_last = "%s-%d(%d).mp3" % (path, jj, len(ts))

            # 多线程预下载下一段落
            download_t = threading.Thread(target=download_thread,
                                          args=(ts[jj], file_last))
            download_t.start()

            play_t.join()
            download_t.join()

        print("\n====最后")
        # 把最后一段下载好的播放
        play_thread(file_last)


# 测试tts和mpv播放音频
def test_play():
    txt = "恭喜！配置成功！快打开阅读app，并修改ip地址吧！"
    file = "test.webm"
    download_thread(txt, file)
    play_thread(file)


# test_play()
main()
