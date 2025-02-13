
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

# correct duplicating
duplicate_map = {
    "♪ ♪": " ♪ ",
    "¿ ¿": " ¿ ",
    ", ,": " , ",
    ". .": " . ",
    "? ?": " ? ",
    "! !": " ! ",
    ": :": " : ",
    "; ;": " ; ",
}

# spacing again
punc_spacing_map = {
    " ,": ",",
    " .": ".",
    " ?": "?",
    " !": "!",
    " :": ":",
    " ;": ";",
    "¿ ": "¿",
    "♪ ": "♪",
    " ♪": "♪"
}

parenthesis_map = {
    " \"": "\" ",
    " (": ") ",
    " [": "] ",
    " <": "> ",
}

def auto_correct_with_map(text: str, mapping: dict[str,str]):
    for old, new in mapping.items():
        text = text.replace(old, new)
    if text.count("\n") > 1:
        text_list = [a.strip() for a in text.split("\n")]
        text = " ".join(text_list)
    if "\n" in text:
        text_list = [a.strip() for a in text.split("\n")]
        text = "\n".join(text_list)   
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def auto_correct_line_breaking(text: str, max_length: int = 0) -> str:
    lines = [line.strip() for line in text.splitlines()]
    text = " ".join(lines).strip()
    
    if text.startswith("-"):
        break_point = text.find(" -")
        if not break_point == -1:
            first_line = text[:break_point].strip()
            second_line = text[break_point:].strip()
            text = first_line + "\n" + second_line
        return text.strip()
        
    elif text.startswith("(") and text.count("(") == 1:
        break_point = text.find(")")
        if not break_point == -1:
            first_line = text[:break_point + 1].strip()
            second_line = text[break_point + 1:].strip()
            text = first_line + "\n" + second_line
        return text.strip()
    
    elif max_length and len(text) > max_length:   
        break_point = text.find(' ', round(len(text) / 2), len(text))

        if break_point == -1:
            break_point = round(len(text) / 2)
        
        first_line = text[:break_point].strip()
        second_line = text[break_point:].strip()
        text = first_line + "\n" + second_line
        return text.strip()
    
    else:
        return text

def auto_correct(text:str):
    text = auto_correct_with_map(text,punctuation_map)
    text = auto_correct_with_map(text,duplicate_map)
    text = auto_correct_with_map(punc_spacing_map)
    text = auto_correct_line_breaking(text, 48)
    return text