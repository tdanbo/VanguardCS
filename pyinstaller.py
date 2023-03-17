import os
import subprocess
import shutil

print(os.path.isfile("src/main.spec"))

subprocess.call("pyinstaller src/main.spec", shell=True)

# for item in os.listdir("dist"):
#     shutil.move(os.path.join("dist", item), item)

# shutil.rmtree("dist")
# shutil.rmtree("build")
