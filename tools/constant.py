'常量'
from servers import Server
from servers.legado import LegadoServer
from tts import TTS
from tts.edge import EdgeTTS
from tts.ms_azure import AzureTTS


def get_servers() -> list[Server]:
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        LegadoServer(),
    ]


def get_ttses() -> list[TTS]:
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        EdgeTTS(),
        AzureTTS(),
    ]
