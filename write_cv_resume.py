# write_cv_resume.py
import sys
import json
from jinja2 import Environment, FileSystemLoader

def emphasize_any_keywords(v: str, keywords: list):
    replacement = ''
    for keyword in keywords:
        # TODO find the keyword inside a longer string of words
        # but for now, just compare as if it was a single word
        if v.casefold() == keyword:
            replacement = '<b>' + v + '</b>'
            print(replacement)
    return replacement

def dict_emphasize_keywords(d: dict, keywords: list) -> dict:
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_emphasize_keywords(v, keywords)
        elif isinstance(v, list):
            v = list_emphasize_keywords(k, v, keywords)
        elif isinstance(v, str):
            # do not emphasize keywords that are not in these json attributes
            if k not in ['summary','highlight','subhighlights','keywords']:
                continue
            replacement = emphasize_any_keywords(v, keywords)
            if len(replacement):
                d[k] = replacement
    return d

def list_emphasize_keywords(json_attr: str, l: list, keywords: list) -> list:
    for i,e in enumerate(l):
        if isinstance(e, list):
            e = list_emphasize_keywords(e, keywords)
        elif isinstance(e, dict):
            e = dict_emphasize_keywords(e, keywords)
        elif isinstance(e, str):
            if json_attr not in ['summary','highlight','subhighlights','keywords']:
                continue
            replacement = emphasize_any_keywords(e, keywords)
            if len(replacement):
                l[i] = replacement
    return l

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
            if len(line.strip()): keywords.append(line.strip().casefold())
except (OSError):
    pass
print ("Keywords to be emphasized:", keywords)

# emphasize keywords in resume_data
output = dict_emphasize_keywords(resume_data, keywords)


# print (resume_data)
environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("cv_resume.txt.jinja")

content = template.render(resume_data)

filename = root + "_resume.html"
with open(filename, mode="w", encoding="utf-8") as message:
    environment.parse(template)
    message.write(content)
    print(f"... wrote {filename}")
