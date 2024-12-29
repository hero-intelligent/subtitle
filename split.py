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

ass_data = parse_ass_file("c:/Users/hero/Desktop/20241229/Starlight Boys/直播1/EP10_ 总决赛现场直播 九位少年成团出道.完整版.ass")

ass_events = ass_data["Events"]

ass_events_1 = ass_events[:1570]
ass_events_2 = ass_events[1570:2670]
ass_events_3 = ass_events[2670:3770]
ass_events_4 = ass_events[3770:4400]
ass_events_5 = ass_events[4400:5030]
ass_events_6 = ass_events[5030:6290]
ass_events_7 = ass_events[6290:6920]
ass_events_8 = ass_events[6920:7710]
ass_events_9 = ass_events[7710:]

ass_data_1 = copy.deepcopy(ass_data)
ass_data_2 = copy.deepcopy(ass_data)
ass_data_3 = copy.deepcopy(ass_data)
ass_data_4 = copy.deepcopy(ass_data)
ass_data_5 = copy.deepcopy(ass_data)
ass_data_6 = copy.deepcopy(ass_data)
ass_data_7 = copy.deepcopy(ass_data)
ass_data_8 = copy.deepcopy(ass_data)
ass_data_9 = copy.deepcopy(ass_data)

ass_data_1["Events"] = ass_events_1
ass_data_2["Events"] = ass_events_2
ass_data_3["Events"] = ass_events_3
ass_data_4["Events"] = ass_events_4
ass_data_5["Events"] = ass_events_5
ass_data_6["Events"] = ass_events_6
ass_data_7["Events"] = ass_events_7
ass_data_8["Events"] = ass_events_8
ass_data_9["Events"] = ass_events_9

str_1 = json_to_srt(ass_data_1,not_keep_index=False)
str_2 = json_to_srt(ass_data_2,not_keep_index=False)
str_3 = json_to_srt(ass_data_3,not_keep_index=False)
str_4 = json_to_srt(ass_data_4,not_keep_index=False)
str_5 = json_to_srt(ass_data_5,not_keep_index=False)
str_6 = json_to_srt(ass_data_6,not_keep_index=False)
str_7 = json_to_srt(ass_data_7,not_keep_index=False)
str_8 = json_to_srt(ass_data_8,not_keep_index=False)
str_9 = json_to_srt(ass_data_9,not_keep_index=False)

with open("1-1570.srt", "w", encoding="utf-8") as file:
    file.write(str_1)
with open("1571-2670.srt", "w", encoding="utf-8") as file:
    file.write(str_2)
with open("2671-3770.srt", "w", encoding="utf-8") as file:
    file.write(str_3)
with open("3771-4400.srt", "w", encoding="utf-8") as file:
    file.write(str_4)
with open("4401-5030.srt", "w", encoding="utf-8") as file:
    file.write(str_5)
with open("5031-6290.srt", "w", encoding="utf-8") as file:
    file.write(str_6)
with open("6291-6920.srt", "w", encoding="utf-8") as file:
    file.write(str_7)
with open("6921-7710.srt", "w", encoding="utf-8") as file:
    file.write(str_8)
with open("7711-8340.srt", "w", encoding="utf-8") as file:
    file.write(str_9)















