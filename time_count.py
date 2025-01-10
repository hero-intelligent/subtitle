from file_io import parse_docx_file
from file_io import parse_ass_file
from file_io import parse_srt_file
from file_io import json_to_word
from file_io import json_to_ass
from file_io import json_to_srt
from file_io import timestamp_reform
from docx import Document
import copy
import json

import sys
import os
import re

import traceback

import pandas as pd

from datetime import datetime

def time_to_timestamp(time_str):
    time_pattern = r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
    # 匹配时间字符串
    match = re.match(time_pattern, time_str)
    if match:
        # 提取时、分、秒和毫秒
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        milliseconds = int(match.group(4))
        
        # 获取当前日期
        now = datetime.now()

        # 创建一个时间对象，假设是今天的日期
        time_obj = now.replace(hour=hours, minute=minutes, second=seconds, microsecond=milliseconds * 1000)

        # 将该时间转换为时间戳（自1970年1月1日以来的秒数）
        timestamp = (time_obj - datetime(1970, 1, 1)).total_seconds()
        
        return timestamp
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def process(file_path):
    if file_path.endswith("ass"):
        data = parse_ass_file(file_path)
    elif file_path.endswith("srt"):
        data = parse_srt_file(file_path)

    events = data["Events"]

    nested_data = []
    for event in events:
        line = {}
        line["Index"] = event["Index"]
        line["Start"] = timestamp_reform(event["Start"])
        line["End"] = timestamp_reform(event["End"])
        
        timestamp_start = time_to_timestamp(line["Start"])
        timestamp_end = time_to_timestamp(line["End"])
        line["During"] = timestamp_end - timestamp_start

        line["Text"] = event["Text"]

        nested_data.append(line)

    df = pd.DataFrame(nested_data)

    df.to_excel(f'{file_path}.xlsx', index=False)

def main():
    # 获取命令行参数
    args = sys.argv[1:]

    # 遍历传入的参数并进行分类
    for arg in args:
        process(arg)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An error occurred:", file=sys.stderr)
        print(e, file = sys.stderr)
        traceback.print_exc(file=sys.stderr)

    input("\n\nPress Enter to exit.")