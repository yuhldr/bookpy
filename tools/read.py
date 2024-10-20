'统计阅读时间'
from datetime import datetime

from tools import get_data, save_data
from tools.config import PATH_CONFIG_DIR

PATH_READ_TIME = f"{PATH_CONFIG_DIR}/read_time.json"


def save_read_time(date_k, read_time_data, book_name):
    """保存阅读时间，每一天是一个key，每天可以多本书，每本书多次阅读，每次阅读多个时长间隔

    Args:
        date_k (str): 开始阅读时间
        date_v (list[int]): 每个循环阅读时间

    Returns:
        dict: {2024-10-20:{'2024-10-20 10:40:31': [1, 2, 3]}}
    """

    # 获取当前日期，只保留年月日
    today_key = str(datetime.now().date())

    data = get_data(PATH_READ_TIME, {})

    if today_key not in data:
        data[today_key] = {book_name: {date_k: read_time_data}}

    if book_name not in data[today_key]:
        data[today_key][book_name] = {date_k: read_time_data}

    # 时间列表一定替换，因为每次阅读date_k不一样，但是不同循环date_k一样
    data[today_key][book_name][date_k] = read_time_data

    save_data(PATH_READ_TIME, data)


def count_read_time():
    """显示详细信息
    """
    data = get_data(PATH_READ_TIME, {})
    book_names = {}
    for data_day, data_book in data.items():
        for book_name, data_time in data_book.items():
            if book_name not in book_names:
                book_names[book_name] = {
                    "read_time": 0,
                    "read_word": 0,
                    "days": {}
                }

            book_names[book_name]["days"][data_day] = {
                "read_time": 0,
                "read_word": 0
            }
            for _time_k, time_v in data_time.items():
                book_names[book_name]["read_time"] += sum(time_v["time"])
                book_names[book_name]["read_word"] += sum(time_v["word"])
                book_names[book_name]["days"][data_day]["read_time"] += sum(
                    time_v["time"])
                book_names[book_name]["days"][data_day]["read_word"] += sum(
                    time_v["word"])

    print(list(book_names.keys()))

    for book_name, data in book_names.items():
        s = f"\n***** {book_name} *****\n"
        s += f"总阅读时间：{data['read_time']:.5}秒"
        s += f"，总阅读字数：{data['read_word']}个"
        for day, d in data["days"].items():
            s += f"\n{day}，阅读时间：{d["read_time"]:.5}秒"
            s += f"，阅读字数：{d["read_word"]}个"
        print(s)
