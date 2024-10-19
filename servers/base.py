'基础类'

class Server:
    """获取待阅读文本的基础类
    """

    def __init__(self, key: str):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """

        self.test = False
        self.key = key
        print(key)

    async def initialize(self):
        """异步初始化一些操作

        Returns:
            str: 比如书名等待阅读的文本
        """
        return "initialize"

    async def next(self):
        """接下来要阅读的文本，并保存本地阅读进度等信息
        """
        print("next")

    async def back(self):
        """暂时没用
        """
        print("back")
