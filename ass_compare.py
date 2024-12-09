import re
from docx import Document

def read_ass_file(file_path):
    """读取ASS文件，返回包含所有Dialogue的行及其相关信息"""
    dialogues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # 只处理 [Events] 部分的 Dialogue 行
            if line.startswith('Dialogue'):
                # 匹配 Dialogue 行中的各个信息
                match = re.match(r'Dialogue:\s*(\d+),([^,]+),([^,]+),([^,]+),[^,]+,[^,]+,[^,]+,[^,]+,,(.*)', line)
                if match:
                    row = {
                        'line_num': line_num,  # 行号
                        'start_time': match.group(2),  # 开始时间
                        'end_time': match.group(3),  # 结束时间
                        'subtitle': match.group(5).strip()  # 字幕内容
                    }
                    dialogues.append(row)
    return dialogues

def compare_subtitles(old_subtitles, new_subtitles):
    """对比两个字幕列表，返回一个包含差异的列表"""
    comparison = []
    max_len = max(len(old_subtitles), len(new_subtitles))
    
    for i in range(max_len):
        old_sub = old_subtitles[i] if i < len(old_subtitles) else None
        new_sub = new_subtitles[i] if i < len(new_subtitles) else None
        
        if old_sub and new_sub:
            comparison.append((
                old_sub['line_num'],  # 行号
                f"{old_sub['start_time']} --> {old_sub['end_time']}",  # 时间段
                old_sub['subtitle'],  # 初版字幕
                new_sub['subtitle']   # 终版字幕
            ))
        elif old_sub:
            # 如果旧字幕有，新的字幕没有
            comparison.append((
                old_sub['line_num'], 
                f"{old_sub['start_time']} --> {old_sub['end_time']}", 
                old_sub['subtitle'], 
                ''  # 没有终版字幕
            ))
        elif new_sub:
            # 如果新的字幕有，旧的字幕没有
            comparison.append((
                new_sub['line_num'], 
                f"{new_sub['start_time']} --> {new_sub['end_time']}", 
                '',  # 没有初版字幕
                new_sub['subtitle']
            ))

    return comparison

def generate_docx(comparison_data, output_path):
    """生成包含对比数据的DOCX文件"""
    doc = Document()
    table = doc.add_table(rows=1, cols=4)
    
    # 添加表头
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '行号'
    hdr_cells[1].text = '00:00:00,000 --> 00:00:00,000'
    hdr_cells[2].text = '初版字幕'
    hdr_cells[3].text = '终版字幕'
    
    # 填充表格
    for row in comparison_data:
        row_cells = table.add_row().cells
        row_cells[0].text = str(row[0])  # 行号
        row_cells[1].text = row[1]  # 时间段
        row_cells[2].text = row[2]  # 初版字幕
        row_cells[3].text = row[3]  # 终版字幕

    # 保存文件
    doc.save(output_path)

def main():
    old_ass_path = 'old.ass'  # 旧版ASS文件路径
    new_ass_path = 'new.ass'  # 终版ASS文件路径
    output_path = 'subtitle_comparison.docx'  # 输出DOCX文件路径
    
    # 读取初版和终版ASS文件并提取字幕信息
    old_subtitles = read_ass_file(old_ass_path)
    new_subtitles = read_ass_file(new_ass_path)
    
    # 对比两个字幕文件并生成数据
    comparison_data = compare_subtitles(old_subtitles, new_subtitles)
    
    # 生成DOCX文件
    generate_docx(comparison_data, output_path)
    print(f"对比结果已保存为 {output_path}")

if __name__ == '__main__':
    main()
