import re

class SubtitleProcessor:
    def __init__(self, original_ass, translated_ass, modified_ass):
        self.original_ass = self.read_ass_file(original_ass)
        self.translated_ass = self.read_ass_file(translated_ass)
        self.modified_ass = self.read_ass_file(modified_ass)

    def read_ass_file(self, filename):
        """
        读取ASS文件内容，返回字幕行的列表
        """
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    def compare_subtitles(self):
        """
        比较原文和改后原文的差异，生成待改译文
        """
        result_lines = []
        for orig_line, mod_line, trans_line in zip(self.original_ass, self.modified_ass, self.translated_ass):
            # 仅在原文与改后原文不同的情况下生成待改译文
            if orig_line != mod_line:
                # 查找对应的原译文字幕内容
                result_line = self.generate_pending_translation(orig_line, mod_line, trans_line)
                result_lines.append(result_line)
        return result_lines

    def generate_pending_translation(self, orig_line, mod_line, trans_line):
        """
        生成待改译文字幕行，标记出有变动的内容
        """
        # 仅将改动的部分替换为待改译文
        # 可以根据需要，选择如何格式化输出待改译文
        modified_content = mod_line.strip().replace(orig_line.strip(), '[待改译] ' + trans_line.strip())
        return modified_content

    def write_pending_translations(self, output_file):
        """
        将待改译文写入到新的ASS文件
        """
        result_lines = self.compare_subtitles()
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(result_lines)

# 输入文件路径
original_ass_file = 'original.ass'      # 原文ASS
translated_ass_file = 'translated.ass'  # 原译文ASS
modified_ass_file = 'modified.ass'      # 改后原文ASS
output_ass_file = 'pending_translations.ass'  # 待改译文ASS输出路径

# 创建处理器实例
processor = SubtitleProcessor(original_ass_file, translated_ass_file, modified_ass_file)

# 生成并保存待改译文ASS
processor.write_pending_translations(output_ass_file)

print(f"待改译文已保存到: {output_ass_file}")
