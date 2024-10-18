# 摸鱼听书

> 写程序很多时候是重复工作，听音乐没细胞，那就听听书洗洗脑子吧

## 原因

> [阅读app](https://github.com/gedoor/legado) 听书很方便，但是我喜欢带着电脑上的头戴式耳机，所以想在电脑上听书

- 需要结合 [阅读app](https://github.com/gedoor/legado)
- 可以免费用 `微软晓晓听书`
- 阅读进度与手机同步


## 使用方法

如果你在使用 `python3` 下面的很容易

### 环境配置

> 只需配置一次

1. 安装 `python3`

    尽量用linux，windows系统可以用 `WSL`，什么意思，自己百度吧

2. 终端打开到这个目录，安装依赖

    ```python
    pip3 install -r requirements.txt
    ```

3. 播放程序设置

    目前测试了 `mpv` 和 `ffmpeg`，两个都行，选一个

    我用的 linux，比如 `ubuntu`，直接输入 `sudo apt install mpv` 或 `sudo apt install ffmpeg` 即可，其他的自己想办法

    ```bash
    vim ~/.config/bpy/config.json
    ```
    其中
    ```json
    "play":{
        "code": ["ffplay", "-nodisp", "-autoexit", "-loglevel", "info"]
    },
    ```

    修改 `code` 对应的值，比如，如果使用 `mpv` 可以改成如下

    ```json
    "play":{
        "code": ["mpv"]
    },
    ```

4. 测试是否修改成功

    打开 [main.py](main.py)，最后一行 `main()` 改成 `test_play()`，然后运行这个文件，如果听到声音，说明环境配置成功！

    > 注意，测试以后，把刚才修改的 `test_play()` 改回来 `main()`

### 开始使用

1. 打开 `阅读app` 的web服务

    手机与电脑同一个`局域网`，然后打开 [阅读app](https://github.com/gedoor/legado)，设置中点开 `Web服务`，注意那个ip地址（`:` 后面是端口）

2. 修改本地配置文件
    
    ```bash
    vim ~/.config/bpy/config.json
    ```
    其中
    ```json
    "ip": "192.168.1.6",
    "port": "1122"
    ```
    里面的 `192.168.1.6` 改成刚才你看到的 `ip`，端口 `1122` 一般不用改

3. 运行

    运行 [main.py](main.py) 即可


### 其他配置

配置文件路径

```bash
~/.config/bpy/config.json
```

完整配置文件

```json
{
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
            "key": "azure",
            "edge": {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+30%"
            },
            "azure": {
                "key": "你自己的密钥xxxxx",
                "region": "你申请的区域比如：japanwest",
                "language": "zh-CN",
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+30%"
            }
        }
    }
}
```

其中

- tts-edge

    > 免费，不用设置密钥，但是音色少

    ```py
    {
        # 支持的语言和音色：edge-tts --list-voices
        "voice": "zh-CN-XiaoxiaoNeural",
        # 语速
        "rate": "+30%"
    }
    ```

    推荐的音色：
    - XiaoxiaoNeural

- azure

    > 学生有免费额度，必须申请并设置密钥🔑，音色更多

    ```py
    {
        # 密钥必须设置
        "key": "你自己的密钥xxxxx",
        # 区域与你申请密钥选择的区域有关
        "region": "你申请的区域比如：japanwest",
        # 看这里多语言、语音选择：https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts
        "language": "zh-CN",
        "voice": "zh-CN-XiaoxiaoNeural",
        # 语速
        "rate": "+30%"
    }
    ```

    推荐的音色：
    - XiaoxiaoNeural
    - XiaochenNeural
    - XiaochenMultilingualNeural
    - XiaoshuangNeural
    - XiaoyouNeural



## 贡献说明

请保证严格遵守 `pylint`

```bash
pylint $(git ls-files '*.py')
```

## 后续开发说明

- 大概会做ui
- 大概会做朗读本地pdf、txt等格式文本
