"""阅读本地txt文件"""
import datetime
import json
import os
import time

from servers import Server
from tools import cal_file_md5, split_text
from tools.cache import get_cache_path

PATH_FILE = "path_file"


class TxtServer(Server):
    """阅读app相关的webapi"""

    def __init__(self):
        """初始化应用API

        Args:
            conf (dict): 配置 conf["legado"]
        """
        # 书籍位置
        self.path_file = ""

        # 要阅读的，并且分割好的文本list
        self.txts = []
        # 当前读到txts的第几个了
        self.txt_n = 0
        # 每个 txt_n 对应的在原文中的位置
        self.p2s = []
        super().__init__("txt")

    async def initialize(self):
        """异步初始化"""
        if PATH_FILE not in self.conf:
            return "没有设置待阅读的文件所在路径"

        self.path_file = self.conf[PATH_FILE]
        print(self.path_file)

        pos = self.get_book_progress()["pos"]
        print(f"上次读取的位置：{pos}")

        with open(self.path_file, "r", encoding="utf-8") as f:
            self.txts, self.p2s, self.txt_n = split_text(f.read(), pos)

        return "开始"

    async def next(self):
        """下一步

        Returns:
            _type_: _description_
        """

        txt = self.txts[self.txt_n]
        await self.save_book_progress()
        self.txt_n += 1
        return txt

    async def get_book_progress(self):
        """异步保存阅读进度
        """

        md5 = cal_file_md5(self.path_file)
        cache_path = f"{get_cache_path()}/{md5}.json"
        if not os.path.exists(cache_path):
            print(f"进度文件不存在: {cache_path}")
            return {PATH_FILE: self.path_file, "date": 0, "pos": 0}

        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data[PATH_FILE] != self.path_file:
                print(f"文件位置不一致：{data[PATH_FILE]} -> {self.path_file}")

            return data

    async def save_book_progress(self):
        """异步保存阅读进度

        Args:
            book_data (dict): 书籍信息

        Raises:
            ValueError: 当进度保存出错时抛出异常
        """
        # 获取当前时间戳（毫秒）
        dct = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)

        # 构建请求数据
        data = {
            PATH_FILE: self.path_file,
            "date": dct,
            "pos": self.p2s[self.txt_n],
        }

        md5 = cal_file_md5(self.path_file)
        cache_path = f"{get_cache_path()}/{md5}.json"
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
