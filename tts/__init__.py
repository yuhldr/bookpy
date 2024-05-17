"""一些工具"""
import copy
import os
import subprocess

from tts.edge import download_mp3 as edge_download

TTS_EDGE = "edge"


def get_tts_ds(conf: dict):
    """下载相关配置

    Args:
        conf (dict): 所配置

    Returns:
        _type_: _description_
    """
    return conf["tts"]["download"]


def get_td_key(conf_tts_download: dict):
    """哪个下载服务

    Args:
        conf_tts_download (dict): _description_

    Returns:
        _type_: _description_
    """
    return conf_tts_download["key"]


def get_td(conf):
    """获取当前选择的下载服务

    Args:
        conf (dict): 完整配置

    Returns:
        _type_: _description_
    """
    ds = get_tts_ds(conf)
    return ds[get_td_key(ds)]


def download_mp3(text, file, conf: dict):
    """下载视频

    Args:
        text (str): 文字
        file (str): 下载到哪里
        cfg (dict): 只要conf["tts"]["download"]的部分

    Returns:
        _type_: _description_
    """
    print(text[:20])
    return edge_download(text, file, get_td(conf))


def play_mp3(file_path, conf: dict):
    """子线程阅读

    Args:
        file_path (_type_): 音频文件路径
    """

    codes = copy.copy(conf["tts"]["play"]["code"])
    codes.append(file_path)

    with subprocess.Popen(codes) as process:
        process.communicate()
    os.remove(file_path)

    # 方便调试，并且可以结合mpv而不是使用ffplay
    # with subprocess.Popen(cfg, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
    #     stdout, stderr = process.communicate()
    #     print("stdout:", stdout.decode())
    #     print("stderr:", stderr.decode())
