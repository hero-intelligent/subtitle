import re




def remove_comments(code):
    # 去除单行注释（以#开头）
    code_no_single_line_comments = re.sub(r'#.*', '', code)

    # 去除多行注释（以'''或"""包裹）
    code_no_multi_line_comments = re.sub(r"'''(.*?)'''|\"\"\"(.*?)\"\"\"", '', code_no_single_line_comments, flags=re.DOTALL)

    return code_no_multi_line_comments

with open("test7.py","r", encoding="utf-8") as p:
    t = p.read()

t = remove_comments(t)

while " \n" in t:
    t = t.replace(" \n", "\n")
while "\n\n" in t:
    t = t.replace("\n\n","\n")

t = t.replace("\ndef","\n\ndef")
t = t.strip()

with open("test7.py", "w", encoding="utf-8") as q:
    q.write(t)