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

3. 终端安装 `mpv`

    我用的 linux，比如 `ubuntu`，直接输入 `sudo apt install mpv` 即可，其他的自己想办法
    
    > windows系统（WSL不需要）可能需要在 [tools/tts.py](tools/tts.py) 修改 `play_thread` 函数的参数 `line_app="mpv"`，`mpv` 改成你的 `mpv命令所在路径`

4. 测试是否修改成功

    打开 [main.py](main.py)，最后一行 `main()` 改成 `test_play()`，然后运行这个文件，如果听到声音，说明环境配置成功！

    > 注意，把刚才修改的 `test_play()` 改回来 `main()`

### 开始使用

1. 打开 `阅读app` 的web服务

    手机与电脑同一个`局域网`，然后打开 [阅读app](https://github.com/gedoor/legado)，设置中点开 `Web服务`，注意那个ip地址

2. 修改`legado.py`

    修改 [servers/legado.py](servers/legado.py)，里面的 `http://192.168.31.5:1122` 改成刚才你看到的 `ip`

3. 运行

    运行 [main.py](main.py) 即可

