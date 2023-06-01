import requests
import urllib
import time
import datetime
import json

# https://github.com/gedoor/legado
# 阅读app ip和端口
host_book = "http://192.168.31.5:1122"


# *******************  阅读app 相关的webapi  *******************
# 获取书架
def get_book_shelf(n=0):
    data = requests.get(host_book + '/getBookshelf').json()["data"]
    # 第几本数，建议不要动，就第一本书就行，
    # 想读某一本书的话，手机上点一下那本书
    return data[n]


def data2url(book_data):
    return urllib.parse.quote(book_data["bookUrl"])


# 获取书某一章节的文本
def get_book_txt(book_data, index=0):
    url = "%s/getBookContent?url=%s&index=%d" % (host_book,
                                                 data2url(book_data), index)
    response_j = requests.get(url).json()
    return response_j["data"]


# 获取书章节目录
def getChapterList(book_data):
    url = "%s/getChapterList?url=%s" % (host_book, data2url(book_data))
    rp = requests.get(url)
    return rp.json()["data"]


# 保存读取进度
def saveBookProgress(book_data):
    dct = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    data = {
        "name": book_data["name"],
        "author": book_data["author"],
        "durChapterIndex": book_data["durChapterIndex"],
        "durChapterPos": book_data["durChapterPos"],
        "durChapterTime": dct,
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
    else:
        print("章节：%d  同步读取进度：%d" %
              (data["durChapterIndex"], data["durChapterPos"]))


# *******************  阅读app 相关的webapi  *******************
