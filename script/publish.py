#! /bin/env python3.6
import pandoc
import sys
import os


def load_version():
    with open('VERSION') as fh:
        res = fh.read()
    return res


version = load_version()

# force tag the repo
rc = os.system(f'git rev-parse -q --verify "refs/tags/{version}"')

if rc == 0:
    # tag already exists, delete it locally and remotely
    os.system(f'git tag -d {version}')
    os.system(f'git push origin :refs/tags/{version}')

rc = os.system(f'git tag {version}')
if rc != 0:
    print('Unable to tag repo!')
    sys.exit(1)

rc = os.system(f'git push --tags')
if rc != 0:
    print('Unable to push tags!')
    sys.exit(1)

# create a rst
doc = pandoc.Document()
doc.markdown = open('README.md', 'rb').read()
f = open('README.rst', 'wb')
f.write(doc.rst)
f.close()
# test upload
rc = os.system("python setup.py sdist upload -r pypitest")

if rc != 0:
    print('Problem uploading to test server!')
    sys.exit(1)

# upload for real
rc = os.system("python setup.py sdist upload -r pypi")
os.remove('README.rst')
sys.exit(rc)
