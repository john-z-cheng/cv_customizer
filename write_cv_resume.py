
# write_cv_resume.py
import argparse
import re
import sys
import json
from jinja2 import Environment, FileSystemLoader

emphasized_attributes = ['summary','highlights','highlight','subhighlights','keywords']

def emphasize_any_keywords(v: str, keywords: list):
    replacement = ''
    match_qty = 0
    for keyword in keywords:
        if match_qty:
            pass
        regex = rf"\b{keyword}\b"
        # keywords have already been casefolded but the value has not
        p = re.compile(regex, re.IGNORECASE)
        matches = p.finditer(v)
        left_idx = 0
        found = False
        for match in matches:
            match_qty += 1
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
        # next keyword search should use modified replacement
        if found:
            v = replacement
            print('replacement: ',v)
            replacement = ''
    # return the last modified replacement
    if match_qty:
        return v
    else:
        return ''

def dict_emphasize_keywords(d: dict, keywords: list) -> dict:
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_emphasize_keywords(v, keywords)
        elif isinstance(v, list):
            v = list_emphasize_keywords(k, v, keywords)
        elif isinstance(v, str):
            # do not emphasize keywords that are not in these json attributes
            if k not in emphasized_attributes:
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
            if json_attr not in emphasized_attributes:
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
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs='?', default='anon', help="produce output using the file named data_for_<root>.txt")
    parser.add_argument("-k", "--keywords", help="emphasize keywords in output using the file named keywords_for_<KEYWORDS>")
    args = parser.parse_args()
    argv = vars(args)
    root = argv['root']
    if argv['keywords']:
        kroot = argv['keywords']
    else:
        kroot = root
    d_file = "data_for_" + root + ".json"
    k_file = "keywords_for_" + kroot + ".txt"
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
