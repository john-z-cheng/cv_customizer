# write_cv_resume.py
import sys
import json
from jinja2 import Environment, FileSystemLoader

root = "anon"
try:
    root = sys.argv[1]
except:
    pass

with open(file="data_for_" + root + ".json", mode="r") as data_file:
    resume_data = json.load(data_file)

# keywords_list contains a keyword (or keyword phrase) on each line
keywords = []
try:
    with open(file="keywords_for_" + root + ".txt", mode="r") as keyword_file:
        for line in keyword_file:
            if len(line.strip()): keywords.append(line.strip())
except (OSError):
    pass
print ("Keywords to be emphasized:", keywords)

# TODO: add bold to keywords in resume_data

# print (resume_data)
environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("cv_resume.txt.jinja")

content = template.render(resume_data)

filename = root + "_resume.html"
with open(filename, mode="w", encoding="utf-8") as message:
    environment.parse(template)
    message.write(content)
    print(f"... wrote {filename}")
