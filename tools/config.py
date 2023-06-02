"""配置"""
import json
import os


def get_config_path():
    """_summary_

    Returns:
        _type_: _description_
    """
    return os.getenv("HOME") + "/.config/bpy/"


if not os.path.exists(get_config_path()):
    os.mkdir(get_config_path())


def get_config():
    """_summary_

    Returns:
        _type_: _description_
    """
    config = {}
    path = f"{get_config_path()}config.json"
    with open(path, "r", encoding="utf-8") as file:
        config = json.load(file)
    return config
