import requests
import urllib
import threading
import os
import shutil
import time
import datetime
import json
import edge_tts
import asyncio
import subprocess
import json

# 阅读app ip和端口
host_book = "http://192.168.31.5:1122"

# 音频文件URL
voice = "zh-CN-XiaoxiaoNeural"
rate = "+12%"
cache_path = 'mp3'


def save_jd(book_data, p):
    json.dump({
        "book": book_data,
        "p": p
    },
              open("jd.json", 'w'),
              indent=4,
              ensure_ascii=False)


# 获取书架
def get_book_shelf(n=0):
    print("get_book_shelf")
    data = requests.get(host_book + '/getBookshelf').json()["data"]
    print(len(data))
    # 第几本数
    return data[n]


def data2url(book_data):
    return urllib.parse.quote(book_data["bookUrl"])


# 获取书的文本
def get_book_txt(book_data, index=0):
    url = "%s/getBookContent?url=%s&index=%d" % (host_book,
                                                 data2url(book_data), index)
    response = requests.get(url)
    save_read_p(book_data, index)
    return response.json()["data"]


def getChapterList(book_data):
    url = "%s/getChapterList?url=%s" % (host_book, data2url(book_data))
    data = requests.get(url).json()["data"]
    return data


# 保存读取进度
def save_read_p(book_data, index):
    current_time = datetime.datetime.now()
    timestamp = int(time.mktime(current_time.timetuple()) * 1000)
    data = {
        "name": book_data["name"],
        "author": book_data["author"],
        "durChapterIndex": index,
        "durChapterPos": 0,
        "durChapterTime": timestamp,
        "durChapterTitle": book_data["durChapterTitle"],
    }

    # 将数据转换为 JSON 格式
    json_data = json.dumps(data)

    # 设置请求头中的 Content-Type 为 application/json
    headers = {'Content-Type': 'application/json'}
    rj = requests.post(host_book + "/saveBookProgress",
                       data=json_data,
                       headers=headers).json()
    if not rj["isSuccess"]:
        raise Exception("进度保存错误！" + rj["errorMsg"])


def split_text(text):
    result = []
    s = ""
    for line in text.strip().split("\n"):
        s += line + "\n"
        if len(s) > 100:
            result.append(s)
            s = ""

    return result


def play_thread(file_path):
    print(file_path)

    with subprocess.Popen([
            "mpv",
            file_path,
    ]) as process:
        process.communicate()
    os.remove(file_path)


async def tts_main(text, file) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(file)


def download_thread(text, file):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tts_main(text, file))
    loop.close()


def test_play():
    txt = "测试一下，你好啊，不不不，我不好"
    file = "test.webm"
    download_thread(txt, file)
    play_thread(file)


def init(book_n, p):
    # 如果文件夹存在，则删除
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)

    # 创建文件夹
    os.mkdir(cache_path)

    try:
        j_data = json.load(open("jd.json", "r"))
        book_data = j_data["book"]
        p = j_data["p"]
        if p > 0:
            p -= 1
    except Exception as e:
        print(e)
        book_data = get_book_shelf(book_n)

    return book_data, p


def main(
    p=0,
    book_n=0,
    dci=-1,
    chap=100,
):
    book_data, p = init(book_n, p)
    cs = getChapterList(book_data)

    if dci < 0:
        dci = book_data["durChapterIndex"]
    for i in range(chap):
        ci = dci + i
        title = cs[ci]["title"]

        path = "%s/%d" % (cache_path, ci)
        book_txt = get_book_txt(book_data, ci)

        ts = split_text(book_txt)
        tsn = len(ts) + 1

        print(len(ts))
        if i == 0:
            ts = ts[p:]

        file_last = "%s.mp3" % (path)
        download_thread(title, file_last)

        for j in range(len(ts)):
            save_jd(book_data, p + j)
            print(p + j)
            play_t = threading.Thread(target=play_thread, args=(file_last, ))
            play_t.start()
            print("play")
            file_last = "%s-%d(%d).mp3" % (path, p + j, tsn)

            download_t = threading.Thread(target=download_thread,
                                          args=(ts[j], file_last))
            download_t.start()

            play_t.join()
            download_t.join()
            print("download")

        play_thread(file_last)


# test_play()
main(p=0)
