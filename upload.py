import os
import re
from copy import copy
from requests.exceptions import HTTPError


def upgrade(add_n=1):
    with open('setup.py', 'r') as f:
        st = f.read()

    pattern = re.compile(r"version=\'(.*)\',")

    version = pattern.search(st).group(1)
    version_new = copy(version.split('.'))

    version_new[2] = str(int(version_new[2]) + add_n)
    version_new = '.'.join(version_new)
    st = st.replace(version, version_new)
    with open('setup.py', 'w') as f:
        f.write(st)


if __name__ == '__main__':
    upgrade(1)
    os.system('rm dist/*')
    os.system('python setup.py sdist bdist_wheel')
    try:
        os.system('twine upload dist/*')
    except HTTPError as e:
        print(e)
        upgrade(-1)
        os.system('rm dist/*')
