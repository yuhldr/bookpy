'''配置'''

from servers.base import Server
from servers.legado import LegadoServer


def get_server(conf) -> Server:
    """基础类的扩展

    Args:
        conf (dict): _description_

    Returns:
        Server: _description_
    """
    conf_servers = conf["server"]
    conf_server_key = conf_servers["key"]
    conf_server = conf_servers[conf_server_key]
    if conf_server_key == "legado":
        return LegadoServer(conf_server)

    print(f"未知的服务 {conf_server_key}")
    return None
