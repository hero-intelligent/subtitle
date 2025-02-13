import re
import warnings
from tqdm import tqdm
import pandas as pd
from package.time_reform import time_str_to_ms, time_ms_to_str
from package.auto_correct import auto_correct


def read(srt_file_path: str) -> dict:
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.lstrip('\ufeff')  # Remove BOM if it's at the start
        content = content.strip()
    
    while "\n\n\n" in content:
        content = content.replace("\n\n\n", "\n\n")
    
    events = []

    pattern = re.compile(r"(\d+\n(?:.*\n)*?)(?=\n\d+\s*\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*\n|\Z)",re.MULTILINE)
    data = pattern.findall(content)

    for line in tqdm(data, desc="parsing srt file"):
        line = line.strip()

        event_data = line.split("\n", 2)  # Split the suptitle into 3 parts

        index = event_data[0]
        start = event_data[1].split("-->",1)[0].strip()
        end = event_data[1].split("-->",1)[1].strip()

        start = time_str_to_ms(start)
        end = time_str_to_ms(end)

        if len(event_data) == 3:
            text = event_data[2].strip()
        else:
            text = ""
            warnings.warn(f"line {index} is empty!", UserWarning)

        event = {
            "Index": index,
            "Start": start,
            "End": end,
            "Text": text
        }
        events.append(event)

    return pd.DataFrame(events)



def generate(events_df: pd.DataFrame) -> str:
    events = events_df.to_dict("records")

    srt_output = []

    for event in tqdm(events, desc="generating srt", total = len(events)):
        index = str(event.get("Index", "")).strip()

        start_time = time_ms_to_str(event["Start"], "srt")
        end_time = time_ms_to_str(event["End"], "srt")

        text = event['Text']
        text = auto_correct(text)

        # Format the SRT entry
        srt_entry = f"{index}\n{start_time} --> {end_time}\n{text}\n"
        srt_output.append(srt_entry)

    return "\n".join(srt_output)

