import json

def parse_ass_to_json(ass_file_path):
    # 用于存储所有的样式信息
    styles = []
    
    with open(ass_file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    # 查找 Format 行和 Style 行
    format_line = None
    style_lines = []

    for line in lines:
        line = line.strip()
        
        # 查找 Format 行
        if line.startswith("Format:"):
            format_line = line.split(":")[1].strip()  # 获取 Format 后面的部分
        # 查找 Style 行
        elif line.startswith("Style:"):
            style_lines.append(line)

    if not format_line:
        raise ValueError("Format line not found in the ASS file.")

    # 解析 Format 行（字段名）
    field_names = [field.strip() for field in format_line.split(",")]

    # 递归解析每个 Style 行
    for style in style_lines:
        # 将 Style 行按逗号分隔（最多分成 len(field_names) 部分）
        fields = style.split(",", len(field_names) - 1)
        
        # 将每个字段与对应的字段名称配对，并生成字典
        style_data = {}
        for i, field in enumerate(fields):
            style_data[field_names[i]] = field.strip()
        
        styles.append(style_data)
    
    # 将样式列表转换为 JSON 格式并返回
    return json.dumps(styles, ensure_ascii=False, indent=4)

# 调用函数并打印输出的 JSON
ass_file_path = "C:\\Users\\hero\\Downloads\\星光闪耀的少年_jp_ptStarlightBoys_EP04_Air_1114\\星光闪耀的少年_jp_ptStarlightBoys_EP04_Air_1114_葡萄牙语_语料ai翻译1.ass"
json_data = parse_ass_to_json(ass_file_path)
print(json_data)

# 如果你想将结果保存到文件，可以使用：
with open('styles.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
