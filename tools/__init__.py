"""一些工具
"""


def split_text(text_all, dcp=0):
    """重新划分段落，防止太短

    Args:
        text_all (dict): 书json
        dcp (int, optional): 分段转音频，第几段. Defaults to 0.

    Returns:
        _type_: result（分割以后的文本数组）, p2s（每个字符在这个章节的索引位置）, n_last（记录的索引位置是第几个分割文本）
    """
    result = []
    p2s = [0]
    text = ""
    n_last = 0

    last = 0
    text_list = text_all.strip().split("\n")
    for i, line in enumerate(text_list):
        text += line + "\n"
        # 至少一段，如果一段没超过100个字，把下一段也连上，还不够100,继续
        # 如果这个章节最后，也算上
        if len(text) > 100 or i == len(text_list) - 1:

            if last <= dcp <= last + len(text):
                n_last = len(result)

            result.append(text)
            # 这个分割是第几个字符，方便保存进度
            p2s.append(last + len(text))

            last = last + len(text)
            text = ""
    print(f"章节分割：{len(result)}|{len(p2s)} 字符索引位置\n{p2s}")

    return result, p2s, n_last-1
