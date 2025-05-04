#!/usr/bin/env python3

import re
import os
import shutil
file_path = os.path.abspath(os.path.join("HSA-backend", "static", "browser", "index.html"))
dest_path = os.path.abspath(os.path.join("HSA-backend", "templates", "index.html"))
print(file_path)
# Read the file contents
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add the Django static loader tag at the top if it's not already present
if "{% load static %}" not in content:
    print("added load")
    content = "{% load static %}\n" + content

# convert src="/static/browser/filename" to src="{% static 'browser/filename' %}"
content = re.sub(r'src="static/angular/([^"]+)"',r'src={% static "\1" %}',content)
#Replace href attributes: convert href="/static/browser/filename" to href="{% static 'browser/filename' %}"
content = re.sub(r'href="static/angular/([^"]+)"',r'href={% static "\1" %}',content)

# Write back the modified content to the file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("File processed successfully!")
print("Moving updated file...")
shutil.move(file_path, dest_path)
print("File copied successfully!")

# --- BEGIN MINIMAL ADDITION: copy all files from static/browser/static → static ---
assets_src  = os.path.abspath(os.path.join("HSA-backend", "static", "browser", "static"))
assets_dest = os.path.abspath(os.path.join("HSA-backend", "static"))

if os.path.isdir(assets_src):
    print(f"Copying assets from {assets_src} to {assets_dest}")
    for root, dirs, files in os.walk(assets_src):
        rel = os.path.relpath(root, assets_src)
        target_dir = os.path.join(assets_dest, rel)
        os.makedirs(target_dir, exist_ok=True)
        for fname in files:
            shutil.copy2(os.path.join(root, fname), os.path.join(target_dir, fname))
    print("All static assets copied.")
else:
    print(f"No assets directory at {assets_src}, skipping copy.")
# --- END MINIMAL ADDITION ---
