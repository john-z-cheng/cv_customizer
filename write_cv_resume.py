# write_cv_resume.py
import re
import sys
import json
from jinja2 import Environment, FileSystemLoader

def emphasize_any_keywords(v: str, keywords: list):
    replacement = ''
    for keyword in keywords:
        regex = rf"\b{keyword}\b"
        # keywords have already been casefolded but the value has not
        p = re.compile(regex, re.IGNORECASE)
        matches = p.finditer(v)
        left_idx = 0
        found = False
        for match in matches:
            found = True
            right_idx = match.start()
            part_str = v[left_idx:right_idx] + '<b>'
            replacement = replacement + part_str
            part_str = v[right_idx:match.end()] + '</b>'
            replacement = replacement + part_str
            left_idx = match.end()
        # if a match was detected, then include remainder of the value
        if found and left_idx < len(v):
            replacement = replacement + v[left_idx:]
            print(replacement)
            break
            # TODO handle the case where two keywords are in a long string,
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

def load_resume_data(data_file):
    with open(file=data_file, mode="r") as data_file:
        raw_data = json.load(data_file)
    return raw_data

def load_keywords(k_filename):
    # keywords_list contains a keyword (or keyword phrase) on each line
    keywords = []
    try:
        with open(file=k_filename, mode="r") as keyword_file:
            for line in keyword_file:
                if len(line.strip()): keywords.append(line.strip().casefold())
    except (OSError):
        pass
    print ("Keywords to be emphasized:", keywords)
    return keywords

def write_resume(resume_data, html_filename):
    environment = Environment(loader=FileSystemLoader("."))
    template = environment.get_template("cv_resume.txt.jinja")

    content = template.render(resume_data)
    with open(html_filename, mode="w", encoding="utf-8") as message:
        environment.parse(template)
        message.write(content)
        print(f"... wrote {html_filename}")

def define_filenames():
    root = "anon"
    try:
        root = sys.argv[1]
    except:
        pass
    d_file = "data_for_" + root + ".json"
    k_file = "keywords_for_" + root + ".txt"
    h_file = root + "_resume.html"
    filenames = (d_file, k_file, h_file)
    print (filenames)
    return filenames

def main():
    d_file, k_file, h_file = define_filenames()
    raw_data = load_resume_data(d_file)
    keywords = load_keywords(k_file)
    resume_data = dict_emphasize_keywords(raw_data, keywords)
    write_resume(resume_data, h_file)

if __name__ == "__main__":
    main()
