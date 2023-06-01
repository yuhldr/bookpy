# 书json
# 分段转音频，第几段
def split_text(text, dcp=0):
    result = []
    p2s = [0]
    s = ""
    p = 0

    last = 0
    text_list = text.strip().split("\n")
    for i, line in enumerate(text_list):
        s += line + "\n"
        # 至少一段，如果一段没超过100个字，把下一段也连上，还不够100,继续
        # 如果这个章节最后，也算上
        if len(s) > 100 or i == len(text_list) - 1:

            if last <= dcp and dcp <= last + len(s):
                p = len(result)

            result.append(s)
            # 这个分割是第几个字符，方便保存进度
            p2s.append(last + len(s))

            last = last + len(s)
            s = ""
    print("章节分割：%d|%d 字符索引位置\n%s" % (len(result), len(p2s), p2s))

    # 分割以后的文本数组
    # 每个字符在这个章节的索引位置
    # 记录的索引位置是第几个分割文本
    return result, p2s, p