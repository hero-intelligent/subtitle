from file_io import parse_docx_file
from file_io import parse_ass_file
from file_io import parse_srt_file
from file_io import json_to_word
from file_io import json_to_ass
from file_io import json_to_srt

from docx import Document
import copy
import json

import sys
import os
import re

import pandas as pd

from datetime import datetime

def combine_match(combined_events: list, translated_events: list) -> None:
    for i, event in enumerate(combined_events):
        translated_text = translated_events[i]["Text"].strip()
        if translated_text != "":
            event["Text"] = translated_text

def combine_not_match(
        combined_events: list,
        untranslated_events: list,
        translated_events: list,
        field_reference = "Text"
        ) -> None:
    field_value_references = []
    for i, event in enumerate(combined_events):
        field_value_references.append(event[field_reference].strip())

    replacements = {}
    for i, event in enumerate(translated_events):
        translated_text = event["Text"].strip()

        untranslated_event = untranslated_events[i]
        field_untranslated: str = untranslated_event[field_reference].strip().replace("\n", "NNNNN")

        if translated_text:
            replacements[field_untranslated] = translated_text

    for i, field in enumerate(field_value_references):
        field_untranslated_to_be_combined = field.strip().replace("\n", "NNNNN")
        if field_untranslated_to_be_combined in replacements:
            combined_events[i]["Text"] = replacements[field_untranslated_to_be_combined]


def find_diff_in_text(path: str, original_texts: list[str], untranslated_texts: list[str], diffs_list: list):
    for i, original_text in enumerate(original_texts):
        untranslated_text = untranslated_texts[i]
        if original_text.strip() != untranslated_text.strip():
            diff = {
                "path": path,
                "index": i,
                "original": original_text,
                "modified": untranslated_text
            }
            diffs_list.append(diff)

def is_timestamp_match(path: str, original_events: list[dict], untranslated_events: list[dict], diffs_list: list = False) -> bool:
    original_texts = []
    for event in original_events:
        original_texts.append(event["Text"])

    untranslated_texts = []
    for event in untranslated_events:
        untranslated_texts.append(event["Text"])

    if len(original_texts) != len(untranslated_texts):
        return False
    # if the diffs_list is not passed, find_diff() will not be called.
    elif diffs_list == False:
        return True
    else:
        find_diff_in_text(path, original_texts, untranslated_texts, diffs_list)
        return True

def translate_combine(original_data: dict, *translated_doc_path: str, match: bool = True):
    original_events = original_data["Events"]

    # Initiate a variable that data will be combined to.
    combined_data = copy.deepcopy(original_data)
    combined_events = combined_data["Events"]

    diffs = []

    want_match = match
    for path in translated_doc_path:
        print(path)
        untranslated_data, translated_data = parse_docx_file(path)

        untranslated_events = untranslated_data["Events"]
        translated_events = translated_data["Events"]

        if want_match:
            match = is_timestamp_match(path, original_events, untranslated_events, diffs)

        if match:
            print("match!")
            print("match!")
            print("match!")
            combine_match(combined_events, translated_events)
        else:
            combine_not_match(combined_events, untranslated_events, translated_events)

    return copy.deepcopy(combined_data), diffs

def find_never_translated(original_data, combined_data):
    original_events = original_data["Events"]
    combined_events = combined_data["Events"]

    never_translated_events = []

    for i, event in enumerate(combined_events):
        event_text = re.sub(r'^[\s\(\)\[\]\{\}<>♫]*|[\s\(\)\[\]\{\}<>♫]*$', '', event["Text"]).strip()
        original_text = re.sub(r'^[\s\(\)\[\]\{\}<>♫]*|[\s\(\)\[\]\{\}<>♫]*$', '', original_events[i]["Text"]).strip()

        if event["Text"] == original_events[i]["Text"]:
            # event["Text"] == ""
            never_translated_events.append(original_events[i])

        if not event_text:
            never_translated_events.append(original_events[i])

    never_translated_data = copy.deepcopy(original_data)
    never_translated_data["Events"] = never_translated_events

    return copy.deepcopy(never_translated_data)

def auto_correct_single(text): 
    punctuation_map = {
        "，": ", ",
        "。": ". ",
        "？": "? ",
        "！": "! ",
        "：": ": ",
        "；": "; ",
        "“": " \"",    "”": "\" ",
        "「": " \"",    "」": "\" ",
        "『": " \"",    "』": "\" ",
        "（": " (",    "）": ") ",
        "【": " [",    "】": "] ",
        "《": " <",    "》": "> ",
        "、": ", ",
        "——": " -- "
    }

    for old, new in punctuation_map.items():
        text = text.replace(old, new)
    
    # correct spacing
    if text.count("\n") > 1:
        text_list = [a.strip() for a in text.split("\n")]
        text = " ".join(text_list)
    if "\n" in text:
        text_list = [a.strip() for a in text.split("\n")]
        text = "\n".join(text_list)   
    while "  " in text:
        text = text.replace("  ", " ")

    punc_spacing_map = {
        " ,": ",",
        " .": ".",
        " ?": "?",
        " !": "!",
        " :": ":",
        " ;": ";",
    }

    for old, new in punc_spacing_map.items():
        text = text.replace(old, new)

    text = text.strip()

    return text

def auto_correct(combined_data):
    events = combined_data["Events"]
    for event in events:
        text = event["Text"]
        text = auto_correct_single(text)
        event["Text"] = text


def drag_and_drop():
    if len(sys.argv) < 3:
        print("Usage: python file_combine.py <path/to/original/subtitle> <path/to/translated/doc> [<path/to/translated/doc> <path/to/translated/doc> <path/to/translated/doc> ...]")
        input("ass or srt along with translated docx required. Only single original ass or srt file allowed.\nPress Enter to exit...")
        sys.exit(1)

    # 获取命令行参数
    args = sys.argv[1:]

    # 初始化变量
    original_path = None
    doc_paths = []

    # 遍历传入的参数并进行分类
    for arg in args:
        if not os.path.exists(arg):
            print(f"Error: ASS file '{arg}' not found.")
            input("Press Enter to exit")
            sys.exit(1)
        elif arg.endswith('.ass'):
            original_path = arg
            original_data = parse_ass_file(arg)
        elif arg.endswith('.srt'):
            original_path = arg
            original_data = parse_srt_file(arg)
        elif arg.endswith('.docx'):
            doc_paths.append(arg)
        else:
            input("ass or srt along with translated docx required. Only single original ass or srt file allowed.\nPress Enter to exit...")
            sys.exit(1)

    if original_path == None:
        input("ass or srt along with translated docx required. Only single original ass or srt file allowed.\nPress Enter to exit...")
        sys.exit(1)

    return original_path, original_data, doc_paths

def main():
    original_path, original_data, doc_paths = drag_and_drop()

    file_directory = os.path.dirname(original_path)
    file_name = os.path.basename(original_path)
    path_split = os.path.splitext(file_name)

    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y%m%d%H%M%S')

    dir_path = file_directory + "/" + formatted_time + "/"
    # Create the directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Directory created: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

    target_path_prefix = dir_path + formatted_time + path_split[0]

    target_path_prefix = target_path_prefix.replace("\\","/")

    combined_data, diffs = translate_combine(original_data, *doc_paths, match=True if len(doc_paths) > 1 else False)

    auto_correct(combined_data)

    with open(target_path_prefix + '_combined.json', 'w', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, ensure_ascii=False, indent=4)

    doc = json_to_word(original_data, combined_data)
    doc.save(target_path_prefix + '_combined.docx')

    never_translated_data = find_never_translated(original_data, combined_data)

    if path_split[1] == ".srt":
        content = json_to_srt(combined_data)
        never_translated_subtitle = json_to_srt(never_translated_data)
        never_translated_doc = json_to_word(never_translated_data)
        never_translated_doc.save(target_path_prefix + '_never_translated.docx')
    elif path_split[1] == ".ass":
        content = json_to_ass(combined_data)
        never_translated_subtitle = json_to_ass(never_translated_data)
        never_translated_doc = json_to_word(never_translated_data)
        never_translated_doc.save(target_path_prefix + '_never_translated.docx')

    with open(target_path_prefix + "_combined" + path_split[1], "w", encoding="utf-8") as file:
        file.write(content)

    with open(target_path_prefix + "_never_translated" + path_split[1], "w", encoding="utf-8") as file:
        file.write(never_translated_subtitle)

    with open(target_path_prefix + "_never_translated.json", "w", encoding='utf-8') as json_file:
        json.dump(never_translated_data, json_file, ensure_ascii=False, indent=4)

    if diffs:
        with open(target_path_prefix + "diffs.json", 'w', encoding='utf-8') as json_file:
            json.dump(diffs, json_file, ensure_ascii=False, indent=4)

        df = pd.DataFrame(diffs)
        df.to_excel(target_path_prefix + "diffs.xlsx", index=False)

if __name__ == '__main__':
    main()
