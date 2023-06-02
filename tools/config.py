"""配置"""
import json
import os


DEFAULT_CONFIG = {
    "server": {
        "legado": {
            "ip": "192.168.31.6",
            "port": "1122"
        }
    },
    "tts": {
        "play": {
            "code": ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]
            # "code": ["mpv"]
        },
        "edge": {
            "voice": "zh-CN-XiaoxiaoNeural",
            "rate": "+15%"
        }
    }
}
FILE_CONFIG = "config.json"


def get_config_path():
    """_summary_

    Returns:
        str: 配置文件夹路径
    """
    return os.getenv("HOME") + "/.config/bpy/"


if not os.path.exists(get_config_path()):
    os.mkdir(get_config_path())


def get_config():
    """_summary_

    Returns:
        dict: 配置数据
    """
    path = f"{get_config_path()}{FILE_CONFIG}"

    if not os.path.exists(path):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config):
    """_summary_

    Args:
        config (dict): 配置数据
    """
    path = f"{get_config_path()}{FILE_CONFIG}"
    with open(path, 'w', encoding="utf-8") as file:
        json.dump(config,
                  file,
                  indent=4,
                  ensure_ascii=False)
