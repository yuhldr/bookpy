"""配置"""
import json
import os

PATH_CONFIG = f'{os.getenv("HOME")}/.config/bpy/'
if not os.path.exists(PATH_CONFIG):
    os.mkdir(PATH_CONFIG)
PATH_CONFIG = f'{PATH_CONFIG}/config.json'

CONFIG_DATA = None


DEFAULT_CONFIG = {
    "version": 1,
    "server": {
        "key": "legado",
        "legado": {
            "ip": "192.168.1.6",
            "port": "1122"
        }
    },
    "tts": {
        "play": {
            "code": [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet"
            ]
        },
        "download": {
            "key": "edge",
            "edge": {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+30%"
            }
        }
    }
}


def get_config(path=PATH_CONFIG):
    """获取配置

    Args:
        path (_type_, optional): _description_. Defaults to PATH_CONFIG.

    Returns:
        dict: 配置数据
    """

    if not os.path.exists(path):
        print("配置文件不存在，已创建默认配置文件")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(path, "r", encoding="utf-8") as file:
        print(f"读取配置文件: {path}")
        data = json.load(file)
        if "version" not in data or data["version"] != DEFAULT_CONFIG["version"]:
            save_config(DEFAULT_CONFIG)
            data = DEFAULT_CONFIG
        print(data["server"]["legado"]["ip"])
        return data


def save_config(config):
    """_summary_

    Args:
        config (dict): 配置数据
    """
    with open(PATH_CONFIG, 'w', encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
