import json
from file_io import *

def json_to_ass(json_data: dict) -> str:
    ass_output = []

    # Write Script Info
    script_info = json_data.get('ScriptInfo', {})

    ass_output.append("[Script Info]")
    for key, value in script_info.items():
        ass_output.append(f"{key}: {value}")
    ass_output.append("")

    # Write Styles
    ass_output.append("[V4+ Styles]")
    ass_output.append("Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding")
    styles = json_data.get('Styles', [])
    for style in styles:
        style_line = ",".join([
            str(style.get("Name", "")).strip(),
            str(style.get("Fontname", "")).strip(),
            str(style.get("Fontsize", "")).strip(),
            str(style.get("PrimaryColour", "")).strip(),
            str(style.get("SecondaryColour", "")).strip(),
            str(style.get("OutlineColour","")).strip(),
            str(style.get("BackColour", "")).strip(),
            str(style.get("Bold", "")).strip(),
            str(style.get("Italic", "")).strip(),
            str(style.get("Underline", "")).strip(),
            str(style.get("StrikeOut", "")).strip(),
            str(style.get("ScaleX", "")).strip(),
            str(style.get("ScaleY", "")).strip(),
            str(style.get("Spacing", "")).strip(),
            str(style.get("Angle", "")).strip(),
            str(style.get("BorderStyle", "")).strip(),
            str(style.get("Outline", "")).strip(),
            str(style.get("Shadow", "")).strip(),
            str(style.get("Alignment", "")).strip(),
            str(style.get("MarginL", "")).strip(),
            str(style.get("MarginR", "")).strip(),
            str(style.get("MarginV", "")).strip(),
            str(style.get("Encoding", "")).strip()
        ])
        ass_output.append(f"Style: {style_line}")
    ass_output.append("")

    # Write Events
    ass_output.append("[Events]")
    ass_output.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    events = json_data.get('Events', [])
    for event in events:
        event_line = ",".join([
            str(event.get("Layer", "")).strip(),
            timestamp_reform(str(event.get("Start", "")).strip(), output_format="ass"),  # SRT style stored, ASS wanted
            timestamp_reform(str(event.get("End", "")).strip(), output_format="ass"),    # SRT style stored, ASS wanted
            str(event.get("Style", "")).strip(),
            str(event.get("Name", "")).strip(),
            str(event.get("MarginL", "")).strip(),
            str(event.get("MarginR", "")).strip(),
            str(event.get("MarginV", "")).strip(),
            str(event.get("Effect", "")).strip(),
            str(event.get("Text", "")).strip().replace("\n","\\N")                       # SRT style stored, ASS wanted
        ])
        ass_output.append(f"Dialogue: {event_line}")

    return "\n".join(ass_output)

# Example usage
input_json_file = 'testfile\X0643_KIRA the World EP02：少年们的 STAR MT 比赛_pt.json'  # Path to the input JSON file
output_ass_file = 'output_test.ass'  # Path to save the output .ass file

# Read the JSON file
with open(input_json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Convert JSON to ASS
ass_data = json_to_ass(json_data)


with open(output_ass_file, 'w', encoding='utf-8') as f:
    f.write(ass_data)


print(f"ASS file has been generated: {output_ass_file}")
