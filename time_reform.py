import re

def time_str_to_ms(time_str: str) -> int:
    """
    Converts a time string in SRT, ASS, or incorrect format to milliseconds.

    The function supports three formats:
    1. SRT format: `hh:mm:ss,SSS` (e.g., "00:02:15,123")
    2. ASS format: `h:mm:ss.ss` (e.g., "1:30:45.67")
    3. Incorrect format with separators `:` or `,` (e.g., "1:30:45:678" or "1:30:45,678")

    The function will:
    - Parse the time string based on the matching format.
    - Convert the time to milliseconds.
    - Return the total time in milliseconds or -1 if the format is invalid.

    Parameters:
        time_str (str): A time string in SRT, ASS, or an incorrect format.

    Returns:
        int: The time in milliseconds if the format is valid, or -1 if the format is invalid.

    Example:
        time_str_to_ms("00:02:15,123")  -> 135123
        time_str_to_ms("1:30:45.67")    -> 544567
        time_str_to_ms("1:30:45:678")   -> 544678 (after fixing)
        time_str_to_ms("25:99:99,999")  -> -1 (invalid format)
    """

    pattern_srt = r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
    pattern_ass = r"^(\d{1,2}):(\d{2}):(\d{2})\.(\d{2})$"
    pattern_wrong = r"^(\d+):(\d{2}):(\d{2})[:.,](\d+)$"

    # 使用正则表达式进行匹配
    match_srt = re.match(pattern_srt, time_str)
    match_ass = re.match(pattern_ass, time_str)
    match_wrong = re.match(pattern_wrong, time_str)

    is_valid = bool(match_srt) or bool(match_ass) or bool(match_wrong)
    if not is_valid:
        return -1
    
    # 如果匹配到 SRT 格式
    if match_srt:
        hours = int(match_srt.group(1))
        minutes = int(match_srt.group(2))
        seconds = int(match_srt.group(3))
        milliseconds = int(match_srt.group(4))

    # 如果匹配到 ASS 格式
    elif match_ass:
        hours = int(match_ass.group(1))
        minutes = int(match_ass.group(2))
        seconds = int(match_ass.group(3))
        milliseconds = int(match_ass.group(4)) * 10

    # 如果匹配到错误格式，尝试修复
    elif match_wrong:
        hours = int(match_wrong.group(1))
        minutes = int(match_wrong.group(2))
        seconds = int(match_wrong.group(3))

        ms_str = match_wrong.group(4)
        ms_str = ms_str[:3] + "." + ms_str[3:]
        ms = float(ms_str)
        milliseconds = int(round(ms))

    is_valid = minutes < 60 and seconds < 60

    if is_valid:
        target = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
        return target
    else:
        return -1

def time_ms_to_str(time: int, output_format: str = "srt") -> str:
    """
    Converts time in milliseconds to a formatted string in either SRT or ASS format.

    Parameters:
        time (int): Time in milliseconds (non-negative integer).
        output_format (str, optional): Desired output format. Can be 'srt' or 'ass'. Default is 'srt'.

    Returns:
        str: Formatted time string in the specified format.

    Raises:
        ValueError: If 'time' is not a non-negative integer, or if 'output_format' is invalid.
    """
    is_valid = isinstance(time, int) and time >= 0
    if not is_valid:
        print(time)
        raise ValueError(f"Unsupported input {time}.")
    
    # 计算总小时、分钟、秒、毫秒（或百分之一秒）
    hours = time // 3600000
    time %= 3600000
    minutes = time // 60000
    time %= 60000
    seconds = time // 1000
    milliseconds = time % 1000

    if output_format == "srt":
        # SRT格式：hh:mm:ss,SSS
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    
    elif output_format == "ass":
        # ASS格式：h:mm:ss.ss
        centiseconds = milliseconds // 10  # 毫秒转换为百分之一秒
        return f"{hours}:{minutes:02}:{seconds:02}.{centiseconds:02}"

    else:
        raise ValueError("Unsupported output format. Please use 'srt' or 'ass'.")

if __name__ == "__main__":
    test_cases = [
        # SRT 格式测试
        ("00:02:15,123", 135123),   # 标准格式，时分秒毫秒
        ("01:05:30,999", 3930999),  # 1小时5分钟30秒999毫秒
        
        # ASS 格式测试
        ("1:30:45.67", 5445670),    # 1小时30分钟45秒67百分之一秒
        ("12:00:01.23", 43201230),  # 12小时0分钟1秒23百分之一秒
        
        # 错误格式测试，尝试修复
        ("3:05:10.123", 11110123),  # 错误格式，点号，修复为正确的格式
        ("5:30:12,456", 19812456),  # 错误格式，逗号，修复为正确的格式
        ("8:20:45.98", 30045980),   # 错误格式，点号，修复为正确的格式

        # 不匹配的格式
        ("12:65:50,000", -1),      # 无效分钟数
        ("25:99:99,999", -1),      # 无效时间（大于24小时）
        ("12:00:60,000", -1),      # 无效秒数
        ("abc", -1),               # 完全不匹配的字符串
    ]

    # 运行测试集并打印结果
    for time_str, expected in test_cases:
        result = time_str_to_ms(time_str)
        if expected == result:
            print(f"Input: {time_str} passed")
        else:
            print(f"Input: {time_str} => Expected: {expected}, Got: {result}")

    for time_str, expected in test_cases:
        timestr_srt = time_ms_to_str(expected, "srt")
        timestr_ass = time_ms_to_str(expected, "ass")
        if time_str == timestr_srt or time_str == timestr_ass:
            print(f"Input: {expected} passed")
        else:
            print(f"Input: {expected} => Expected: {time_str}, Got: {timestr_srt} and {timestr_ass}")

    time_ms_to_str("abc", "srt")
    time_ms_to_str(-1,"srt")