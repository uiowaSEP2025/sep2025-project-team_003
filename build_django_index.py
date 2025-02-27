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
print("copying updated file...")
shutil.move(file_path, dest_path)
print("File copied successfully!")
