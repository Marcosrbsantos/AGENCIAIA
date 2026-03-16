import os

root = r"c:\Users\Admin\Desktop\Agente"
for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.startswith("post_") and filename.endswith(".png"):
            print(os.path.abspath(os.path.join(dirpath, filename)))
