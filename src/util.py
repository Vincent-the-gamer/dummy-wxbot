def get_content_after_tag(msg: str, tag: str):
    # 定位 tag 的起始位置
    index = msg.find(tag)
    if index != -1:
        # 截取 tag 之后的所有内容(不包含tag本身)
        content = msg[index + len(tag):]
        # 可选：去除开头的空白（空格/换行），让内容更干净
        content = content.lstrip()
        return content
    # 未找到 tag 时返回原字符串
    return msg