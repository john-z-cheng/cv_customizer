# cv_customizer

This is a proof of concept project for customizing a resumé (sometimes equivalent to a CV or curriculum vitae). One finds job search advice on the internet (and books) to tailor or target a resumé to an employer's job description. This project provides at least one simple way of doing that by emphasizing keywords by bolding specific keywords. That functionality is combined with the process of creating the resumé with a template and source data.

## Getting Started

This project has a python script that relies on three input files to generate a single output file in HTML. 

### Prerequisites

The things you need before installing the software.

* Python 3
* Jinja2 (templating engine)

### Installation

Once you have set up your python environment as you prefer, such as a virtual environment, then install the templating engine.

```
$ pip install -U Jinja2
```
To confirm that the basic functionality is working, there are some default files:
- data_for_anon.json
- keywords_for_anon.txt

Execute the python script:
```
python write_cv_resume.py
```

There will be some printed output and a new file created (or overwritten if command is repeated):  **anon_resume.html**

## Usage

The python script relies on file naming convention to reduce typing command line arguments.
Basic description of the arguments is provided with the **-h** flag.

Make a copy of data_for_anon.json with a name like "data_for_<yourname>.json" which you can then edit with the actual text that you will want in your resumé. This file's data schema was copied and somewhat modified from https://jsonresume.org, so not everything in it is necessarily included in the final output. The biggest difference is support for a second level of highlights (bullet points).
The other file needed should have a name like "keywords_for_<job>.txt" to contain those keywords (or phrases) that should be bolded in the HTML output. 

Assuming that the above two files are available, the command to run would be:
```
$ python write_cv_resume.py yourname -k job
```
and its output will be: *job_resume.html*

## Acknowledgments
Thanks to the people/companies behind:
  
* https://github.com/pallets/jinja
* https://github.com/jsonresume

