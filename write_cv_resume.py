# write_cv_resume.py
import sys
import json
from jinja2 import Environment, FileSystemLoader

prefix = "anon"
try:
    prefix = sys.argv[1]
except:
    pass

with open(file=prefix + "_resume_schema.json", mode="r") as data_file:
    resume_data = json.load(data_file)

# print (resume_data)
environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("cv_resume.txt.jinja")

content = template.render(resume_data)

filename = prefix + "_resume.html"
with open(filename, mode="w", encoding="utf-8") as message:
    environment.parse(template)
    message.write(content)
    print(f"... wrote {filename}")
