import os
import json


file_path = os.path.join(".", "license.key")

key_json = json.load(open(file_path, "r"))
print(key_json)

