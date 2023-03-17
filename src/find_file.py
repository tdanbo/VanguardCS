import os
import json

current_dir = os.getcwd()
file_path = os.path.join(current_dir, "license.key")

key_json = json.load(open(file_path, "r"))
print(key_json)

