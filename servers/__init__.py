'''配置'''
from tools.config import get_config


def get_config_server():
    """_summary_

    Returns:
        _type_: _description_
    """
    return get_config()["server"]
