#!/usr/bin/env python3

import os
import re
import yaml
import argparse
import base64

from jinja2 import Environment, FileSystemLoader

# https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another
class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def debug(var):
    print(var)
    return ''

def generate_content(yaml_file, template_file):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(THIS_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )
    j2_env.filters['debug'] = debug
    j2_env.filters['encode'] = str.encode
    j2_env.filters['b64encode'] = base64.b64encode
    j2_env.filters['b64decode'] = base64.b64decode

    with open(yaml_file) as yml:
        yml = yaml.load(yml, Loader)

    template = j2_env.get_template(template_file)

    content = str(template.render(yml))
    print(content)

    return yml

if __name__ == '__main__':
    generate_content('values.yaml', 'traefik-wildcard-cert.yaml.j2')
