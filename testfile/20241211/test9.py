def wrap_text_with_one_newline(text, max_length):
    # 先将输入文本按换行符拆分为多行，并去掉每行的前后空白
    lines = [line.strip() for line in text.splitlines()]
    
    # 用来存储处理后的结果
    result = []
    
    # 如果只有一行，直接检查并处理
    if len(lines) == 1:
        line = lines[0]
        if len(line) > max_length:
            # 如果该行长度超过最大限制，则强制在合适的位置换行
            break_point = line.rfind(' ', 0, max_length)
            if break_point == -1:
                break_point = max_length  # 如果找不到空格，按最大长度断开
            result.append(line[:break_point].strip())
            result.append(line[break_point:].strip())
        else:
            result.append(line)
    else:
        # 处理多行文本，保证只有一个换行符
        for line in lines:
            if len(line) <= max_length:
                result.append(line)
            else:
                break_point = line.rfind(' ', 0, max_length)
                if break_point == -1:
                    break_point = max_length  # 强制断开
                result.append(line[:break_point].strip())
                result.append(line[break_point:].strip())
    
    # 返回只有一个换行符的文本
    return ' '.join(result)

# 测试
# text = """这是第一行
# 这是一段需要换行的文本，它包含了多个单词和字符。"""
# max_length = 20
# print(wrap_text_with_one_newline(text, max_length))
text = "0123456789abcdef"
breakpoint = text.find("a9a")
breakpoint = -2
print(text[:breakpoint] + "\n" + text[breakpoint:])