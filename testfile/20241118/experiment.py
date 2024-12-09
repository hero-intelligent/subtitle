# import re
# import warnings

# def timestamp_srt_to_ass(timestamp: str) -> str:
#     """
#     input: 00:24:01,180
#     output: 0:24:01.18
#     """
#     # Split the timestamp by comma
#     if "," in timestamp:
#         time_part, ms_part = timestamp.split(',')
#     elif "." in timestamp:
#         time_part, ms_part = timestamp.split(',')

#     # Convert the milliseconds to two decimal places
#     ms = int(ms_part) / 1000  # Convert milliseconds to seconds
#     ms_rounded = round(ms, 2)  # Round to two decimal places
    
#     # Format the new timestamp
#     return f"{time_part}.{int(ms_rounded * 100)}"  # Multiply by 100 to get two decimal places

# def timestamp_ass_to_srt(timestamp: str) -> str:
#     """
#     input: 0:24:01.18
#     output: 00:24:01,180
#     """
#     # Split the timestamp into time and milliseconds
#     time_part, ms_part = timestamp.split('.')
    
#     # Convert the milliseconds part to integer (multiply by 100 to reverse the decimal shift)
#     ms = int(round(float(f"0.{ms_part}") * 1000))  # Round and convert to integer
    
#     # Format the time part back to "hh:mm:ss"
#     hours, minutes, seconds = time_part.split(':')
    
#     # Return the formatted timestamp in the desired format
#     return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{ms:03}"







# def timestamp_reform(time_str: str, output_format: str = "srt") -> str:
#     pattern_srt = r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
#     pattern_ass = r"^(\d{1,2}):(\d{2}):(\d{2})\.(\d{2})$"
#     pattern_wrong = r"^(\d+):(\d{2}):(\d{2})[:.,](\d+)$"


#     # 使用正则表达式进行匹配
#     match_srt = re.match(pattern_srt, time_str)
#     match_ass = re.match(pattern_ass, time_str)
#     match_wrong = re.match(pattern_wrong, time_str)

#     if match_srt:
#         print("匹配srt成功！")
#         hours = int(match_srt.group(1))
#         minutes = int(match_srt.group(2))
#         seconds = int(match_srt.group(3))
#         milliseconds = int(round(float("0." + match_srt.group(4)) * 1000))
#         print(f"小时: {hours}, 分钟: {minutes}, 秒: {seconds}, 毫秒: {milliseconds}")
#     elif match_ass:
#         print("匹配ass成功！")
#         hours = int(match_ass.group(1))
#         minutes = int(match_ass.group(2))
#         seconds = int(match_ass.group(3))
#         milliseconds = int(round(float("0." + match_ass.group(4)) * 1000))
#         print(f"小时: {hours}, 分钟: {minutes}, 秒: {seconds}, 毫秒: {milliseconds}")
#     elif match_wrong:
#         warnings.warn(f"Invalid format detected: {time_str}", UserWarning)
#         hours = int(match_wrong.group(1))
#         minutes = int(match_wrong.group(2))
#         seconds = int(match_wrong.group(3))
#         milliseconds = int(round(float("0." + match_wrong.group(4)) * 1000))
#         print(f"小时: {hours}, 分钟: {minutes}, 秒: {seconds}, 毫秒: {milliseconds}")
#     else:
#         print(f"{time_str}匹配失败")

#     if output_format == "srt":
#         return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"
#     elif output_format == "ass":
#         return f"{int(hours):01}:{int(minutes):02}:{int(seconds):02}.{int(round(milliseconds / 1000, 2) * 100)}"











# num_float = 1.2345
# result = round(num_float)
# print(result)

# print(f"{0.21:04}")

# # time_str = "00:24:01,180"
# time_str = "00:24:01.189"
# # time_str = "000000:24:01.182310"

# print(type(timestamp_reform(time_str)))
# # print (timestamp_ass_to_srt("0:24:01.18"))



from docx import Document

# 创建一个新的 Word 文档
doc = Document()

# 添加一个有样式的表格
table = doc.add_table(rows=3, cols=3)

# 设置表格样式为 "Table Grid"（表格带网格线）
table.style = 'Table Grid'

# 添加数据
data = [
    ['Alice', 24, '济南'],
    ['Bob', 27, 'Los Angeles'],
    ['Charlie', 22, 'Chicago']
]

for i, row_data in enumerate(data):
    row_cells = table.rows[i].cells
    for j, cell_data in enumerate(row_data):
        row_cells[j].text = str(cell_data)

# 保存文档
doc.save('styled_table.docx')
