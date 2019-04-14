import requests
import json
import sys
from distutils.version import StrictVersion

if len(sys.argv) not in (3, 4):
	print('Usage: check_image_updates.py {dockerhub image name} {current version in use} {suffix to append (optional)}')
	print('Ex: check_image_updates.py python 3.7')
	sys.exit(0)
	
lib_name = sys.argv[1]
cur_version = sys.argv[2]
suffix = f'-{sys.argv[3]}' if len(sys.argv) > 3 else ''
full_name = lib_name + suffix
current_version = StrictVersion(cur_version)

def check_key(check_dict, key, value):
	return (key in check_dict and check_dict[key] == value) or key not in check_dict

tags = requests.get(f'https://registry.hub.docker.com/v2/repositories/{lib_name}/tags?page_size=1024') 
choices = [r['name'] for r in tags.json()['results'] if check_key(r, 'os', 'linux') and check_key(r, 'arch', 'amd64') and r['name'].endswith(suffix)]

newest_version = StrictVersion('0.0')
for choice in choices:
	try:
		version_test = StrictVersion(choice.replace(suffix, ''))
		# Don't care about alpha/beta versions
		if version_test.prerelease:
			continue
		if version_test > newest_version:
			newest_version = version_test
	# StrictVersion parsing will fail if the version has letters or is in a strange format
	except ValueError:
		continue
if current_version < newest_version:
	print(f'{full_name} is out of date. Current version: {current_version} Newest version: {newest_version}')
else:
	print(f'{full_name} is up-to-date')