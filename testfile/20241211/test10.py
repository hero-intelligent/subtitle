def single_line_breaking(text: str, max_length: int) -> str:
    lines = [line.strip() for line in text.splitlines()]
    text = " ".join(lines).strip()

    if text.startswith("-"):
        break_point = text.find(" -")
        if not break_point == -1:
            first_line = text[:break_point].strip()
            second_line = text[break_point:].strip()
            text = first_line + "\n" + second_line
        return text
        
    if len(text) <= max_length:
        return text
    
    break_point = text.find(' ', round(len(text) / 2), len(text))

    if break_point == -1:
        break_point = round(len(text) / 2)
    
    first_line = text[:break_point].strip()
    second_line = text[break_point:].strip()
    
    return f"{first_line}\n{second_line}"

text = """这是第一行
这是一段需要换行的文本，这是一段需要换行的文本，这是一段需要换行的文本，这是一段需要换行的文本， -它包含了多个单词和字符。"""
max_length = 20
print(single_line_breaking(text, max_length))