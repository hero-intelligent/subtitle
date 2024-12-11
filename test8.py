import os

original_path = r"F:\workdir\2-ass_combine\a.json"

file_directory = os.path.dirname(original_path)
file_name = os.path.basename(original_path)
path_split = os.path.splitext(file_name)

dir_path = file_directory + "/" + path_split[0] + "/"
# Create the directory if it doesn't exist
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    print(f"Directory created: {dir_path}")
else:
    print(f"Directory already exists: {dir_path}")

target_path = file_directory + "/" + path_split[0] + "/" + path_split[0] + '_combined.docx'

print(target_path)

with open(target_path, "w", encoding="utf-8") as f:
    f.write("e")