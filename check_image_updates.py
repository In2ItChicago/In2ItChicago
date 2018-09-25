import requests
import json
import sys
from distutils.version import StrictVersion

lib_name = sys.argv[1]
current_version = StrictVersion(sys.argv[2])

def check_key(check_dict, key, value):
	return (key in check_dict and check_dict[key] == value) or key not in check_dict

tags = requests.get(f'https://registry.hub.docker.com/v2/repositories/library/{lib_name}/tags?page_size=1024') 
choices = [r['name'] for r in tags.json()['results'] if check_key(r, 'os', 'linux') and check_key(r, 'arch', 'amd64')]
newest_version = StrictVersion('0.0')
for choice in choices:
	try:
		version_test = StrictVersion(choice)
		if version_test > newest_version:
			newest_version = version_test
	except ValueError:
		continue
if current_version < newest_version:
	print(f'{lib_name} is out of date. Current version: {current_version} Newest version: {newest_version}')
else:
	print(f'{lib_name} is up-to-date')