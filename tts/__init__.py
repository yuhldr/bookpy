"""一些工具
"""
from tools.config import get_config


def get_config_tts():
    """_summary_

    Returns:
        _type_: _description_
    """
    return get_config()["tts"]
