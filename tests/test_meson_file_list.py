import os

import pytest
import sh

from captain_hooks.meson_file_list import main

MESON_BUILD_TMPL = '''
project('pure_python_project',
    version: '1.0',
    license: 'AGPL-3.0-or-later',
)

python = import('python').find_installation()
subdir('ppp')
'''

MESON_BUILD_PYTHON_TMPL = '''
src = ['__init__.py', 'main.py']

python.install_sources(
    src,
    pure: true,
    subdir: 'ppp'
)
'''

PYTHON_MAIN_PY = '''
import sys

def main(args):
    print(args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
'''


@pytest.fixture()
def meson_python_project_dir(tmp_path_factory):
    src_dir = tmp_path_factory.mktemp('ppp')
    os.mkdir(src_dir / 'ppp')
    with open(src_dir / 'meson.build', 'w') as f:
        f.write(MESON_BUILD_TMPL)

    with open(src_dir / 'ppp' / 'meson.build', 'w') as f:
        f.write(MESON_BUILD_PYTHON_TMPL)

    open(src_dir / 'ppp' / '__init__.py', 'w').close()

    with open(src_dir / 'ppp' / 'main.py', 'w') as f:
        f.write(PYTHON_MAIN_PY)

    return src_dir


def test_meson_python(meson_python_project_dir, tmp_path):
    sh.meson(['setup', tmp_path, meson_python_project_dir])
    assert 'meson-info' in os.listdir(tmp_path)


def test_main():
    assert main() == 0
