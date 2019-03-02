from jinja2 import Template
import os
import sys

files = sys.argv[1:]
for file in files:
    rendered = None
    new_file = file.split('.j2')[0]
    if new_file == file:
        print('File ' + file + ' must end in .j2')
        continue

    with open(file, 'r') as f:
        template = f.read()
        rendered = Template(template).render(**dict(os.environ))

    with open(new_file, 'w') as f:
        f.write(rendered)