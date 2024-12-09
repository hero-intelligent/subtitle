import json
from file_io import *

# # Example JSON data (you can replace this with your actual JSON data)
# json_data = """
# {
#   "script_info": {
#     "title": "Example Subtitle",
#     "original_script": "OpenAI",
#     "script_type": "v4.00",
#     "collisions": "Normal"
#   },
#   "events": [
#     {
#       "start": "0:00:01.00",
#       "end": "0:00:04.00",
#       "style": "Default",
#       "text": "Welcome to the world of ASS subtitles!"
#     },
#     {
#       "start": "0:00:05.00",
#       "end": "0:00:08.00",
#       "style": "Default",
#       "text": "Here we are converting to JSON."
#     }
#   ],
#   "styles": [
#     {
#       "name": "Default",
#       "fontname": "Arial",
#       "fontsize": 20,
#       "primary_colour": "&H00FFFFFF",
#       "secondary_colour": "&H00000000",
#       "back_colour": "&H80000000",
#       "bold": -1,
#       "italic": 0,
#       "border_style": 1,
#       "outline": 1.0,
#       "shadow": 0.0,
#       "alignment": 2,
#       "margin_left": 10,
#       "margin_right": 10,
#       "margin_vertical": 10
#     }
#   ]
# }
# """

# # Convert JSON string to Python dictionary
# data = json.loads(json_data)


# def timestamp_srt_to_ass(timestamp):
#     # Split the timestamp by comma
#     time_part, ms_part = timestamp.split(',')
    
#     # Convert the milliseconds to two decimal places
#     ms = int(ms_part) / 1000  # Convert milliseconds to seconds
#     ms_rounded = round(ms, 2)  # Round to two decimal places
    
#     # Format the new timestamp
#     return f"{time_part}.{int(ms_rounded * 100)}"  # Multiply by 100 to get two decimal places

# # # Example usage
# # timestamp = "00:24:01,180"
# # new_timestamp = timestamp_srt_to_ass(timestamp)
# # print(new_timestamp)  # Output: 0:24:01.18

# def timestamp_ass_to_srt(timestamp):
#     # Split the timestamp into time and milliseconds
#     time_part, ms_part = timestamp.split('.')
    
#     # Convert the milliseconds part to integer (multiply by 100 to reverse the decimal shift)
#     ms = int(round(float(f"0.{ms_part}") * 1000))  # Round and convert to integer
    
#     # Format the time part back to "hh:mm:ss"
#     hours, minutes, seconds = time_part.split(':')
    
#     # Return the formatted timestamp in the desired format
#     return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{ms:03}"

# # # Example usage
# # timestamp = "0:24:01.18"
# # new_timestamp = timestamp_ass_to_srt(timestamp)
# # print(new_timestamp)  # Output: 00:24:01,180









# Function to convert JSON to SRT
def json_to_srt(json_data: dict) -> str:
    # print(json_data)
    events = json_data['Events']
    srt_output = []
    
    for i, event in enumerate(events, start=1):
        start_time = str(event.get("Start", "")).strip()  # Convert to SRT time format
        end_time = str(event.get("End", "")).strip()  # Convert to SRT time format

        start_time = timestamp_reform(start_time, output_format="srt")
        end_time = timestamp_reform(end_time, output_format="srt")
        text = event['Text']
        
        # Format the SRT entry
        srt_entry = f"{i}\n{start_time} --> {end_time}\n{text}\n"
        srt_output.append(srt_entry)
    
    return "\n".join(srt_output)

# # Convert the JSON data to SRT format
# srt_data = json_to_srt(data)

# # Output the SRT data to a file
# with open("output.srt", "w") as file:
#     file.write(srt_data)

# print("SRT file has been created: output.srt")

# Example usage
input_json_file = 'testfile/X0643_KIRA the World EP02：少年们的 STAR MT 比赛_pt.json'  # Path to the input JSON file
output_ass_file = 'output_test.ass'  # Path to save the output .ass file

# Read the JSON file
with open(input_json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Convert JSON to ASS
ass_data = json_to_srt(json_data)


with open(output_ass_file, 'w', encoding='utf-8') as f:
    f.write(ass_data)


print(f"ASS file has been generated: {output_ass_file}")