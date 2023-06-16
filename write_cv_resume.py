
# write_cv_resume.py
import argparse
import re
import json
from jinja2 import Environment, FileSystemLoader

emphasized_attributes = ['summary','highlights','highlight','subhighlights','keywords']

def include_this_match(keyword, excludes, v, match):
    if len(excludes) == 0:
        return True
    for exclude in excludes:
        # collect some character positions in strings needed by logic
        offset = exclude.find(keyword)
        idx = match.start()
        exclude_len_after_key = len(exclude)-offset
        value_len_after_key = len(v) - idx
        # case where the keyword is inside the exclude phrase but the match
        # indicates there are not enough characters preceding it to be equal
        # exclude="zzz key zzz" and v="a key bbb ccc" (idx=2, offset=4)
        if idx < offset:
            return True
        # case where the exclude phrase is too long to possibly match
        # exclude="zzz key zzz" and v="something zzz key d" (idx=10,offset=4)
        if exclude_len_after_key > value_len_after_key:
            return True
        potential = v[idx-offset:idx-offset+len(exclude)].casefold()
        if potential == exclude:
            print("excluding: ", exclude)
            return False
    # no exclusion found
    return True

def get_regex_str(keyword):
    # assign default regular expression for keyword
    regex = rf"\b{keyword}\b"
    # check for special characters in keyword
    # support single period character at beginning or middle of word
    pos = keyword.find('.')
    if pos == 0:
        newword = keyword[1:]
        regex = rf"(?<!\S)\.{newword}\b"
    if pos > 0:
        lefthalf = keyword[0:pos]
        righthalf = keyword[pos:]
        regex = rf"\b{lefthalf}\{righthalf}\b"
    return regex

def emphasize_any_keywords(v: str, keywords: list):
    replacement = ''
    match_qty = 0
    for keyword, excludes in keywords:
        regex = get_regex_str(keyword)
        # keywords have already been casefolded but the value has not
        p = re.compile(regex, re.IGNORECASE)
        matches = p.finditer(v)
        left_idx = 0
        found = False
        for match in matches:
            if len(excludes):
                found = include_this_match(keyword, excludes, v, match)
            else:
                found = True
            if found == True:
                match_qty += 1
            else:
                continue
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

def parse_keywords_line(line):
    stripped_line = line.strip().casefold()
    if len(stripped_line) == 0:
        return None
    parts = stripped_line.split('|')
    keyword = parts[0].strip()
    if len(parts) > 1:
        excludes = list(map(str.strip, parts[1:]))
        print(excludes)
    else:
        excludes = []
    return (keyword,excludes)

def load_keywords(k_filename):
    """Each non-blank line in the file will start with a keyword (or phrase) that is
    intended to be emphasized. Optionally, there can be a pipe character | and additional
    strings that follow on that line for those keywords or phrases that should not be
    emphasized (i.e. excluded). This allows a keyword like 'SQL' to be emphasized, but
    'Microsoft SQL Server' would not have its middle word emphasized."""
    # keywords will be filled with a list of tuples where the first item is a keyword string
    # to be emphasized and the second item is a list of strings that should be excluded
    # from emphasis.
    keywords = []
    try:
        with open(file=k_filename, mode="r") as keyword_file:
            for line in keyword_file:
                key_tuple = parse_keywords_line(line)
                if key_tuple != None:
                    keywords.append(key_tuple)
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
    parser = argparse.ArgumentParser(epilog='Unspecified parameters are assigned a value in a hierarchical manner such that the KEYWORDS value is the SOURCE value and the OUTPUT value combines the SOURCE and KEYWORDS value.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("SOURCE", nargs='?', default='anon', help="produce output using the source file named data_for_<SOURCE>.txt")
    parser.add_argument("-k", "--keywords", help="emphasize keywords in output using the file named keywords_for_<KEYWORDS>", default=argparse.SUPPRESS)
    parser.add_argument("-o", "--output", help="name of output file as <OUTPUT>_resume.html", default=argparse.SUPPRESS)
    args = parser.parse_args()
    argv = vars(args)
    source = argv['SOURCE']
    if argv.get('keywords'):
        kroot = argv['keywords']
    else:
        kroot = source
    if argv.get('output'):
        hroot = argv['output']
    else:
        hroot = None
    d_file = "data_for_" + source + ".json"
    k_file = "keywords_for_" + kroot + ".txt"
    if hroot:
        h_file = hroot + "_resume.html"
    else:
        h_file = kroot + "_" + source + "_resume.html"
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
