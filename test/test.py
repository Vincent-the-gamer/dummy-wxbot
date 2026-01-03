def get_content_after_tag(msg: str, tag: str):
    # 定位 tag 的起始位置
    index = msg.find(tag)
    if index != -1:
        # 截取 tag 之后的所有内容（index + len(keyword) 跳过 tag 本身）
        content = msg[index:]
        # 可选：去除开头的空白（空格/换行），让内容更干净
        content = content.lstrip()
        return content
    # 未找到 tag 时返回原字符串
    return msg

# 测试示例
test_msg1 = "前缀内容/help 这是help之后的消息"
test_msg2 = """[4条]#[tokio::main]: /python
这是换行的内容
包含特殊字符！@#"""
test_msg3 = "没有help的字符串"

print("测试1结果：")
print(get_content_after_tag(test_msg1, "/help"))  # 输出：这是help之后的消息
print("-" * 30)

print("测试2结果：")
print(get_content_after_tag(test_msg2, "/python"))  # 输出：这是换行的内容\n包含特殊字符！@#
print("-" * 30)

print("测试3结果：")
print(get_content_after_tag(test_msg3, "/help"))  # 输出：没有help的字符串