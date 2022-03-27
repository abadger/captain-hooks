#!/usr/bin/python -tt
# Copyright: (c) 2022, Toshio Kuratomi <a.badger@gmail.com>
# License: GPL-v3-or-later
"""
`Pre-commit hook <https://pre-commit.com/#plugins>`_ which tries to keep your
`meson.build <https://mesonbuild.com/>`_ files up to date.

.. warning::
    I am not very familiar with meson yet.  My current needs are to handle
    Python projects so this script only handles those (and only my specific
    use case right now).  If you run across this and want to start using it in
    your project, you may have to do some coding to get it to work.  I'd be
    very happy if you'd show me how to improve this to match the actual
    design of meson for building for other languages rather than my
    half-guesses at what would be useful.
"""
import argparse
import itertools
import json
import os
import re
import subprocess
import sys
import tempfile

from . import compat

PATTERNS = {
    'c': (r'\.c', r'\.h'),
    'cpp': (r'\.cc', '.cpp', 'h', '.hpp'),
    'cython': (r'\.pyx', ),
    'd': (r'\.d', ),
    'fortran': (r'\.f', r'\.for', '.f90', '.f95', '.f03'),
    'java': (r'\.java', ),
    'python': (r'\.py', ),
    'rust': (r'\.rs', ),
    'vala': (r'\.vala', r'\.h'),
    }

TESTS_PATTERNS = ('/tests/', '/test/')
TEST_RE = re.compile('^.*({}).*'.format('|'.join(TESTS_PATTERNS)))

SRC_RES = {k: re.compile('^.*({})$'.format('|'.join(v))) for k, v in PATTERNS.items()}

PATTERN_FRAGMENT = '|'.join(itertools.chain(*(v for v in PATTERNS.values())))
DEFAULT_INCLUDE_RE = re.compile(f'^.*({PATTERN_FRAGMENT})$')


class Validator:
    """Class to validate that given filenames are listed in meson.build files."""

    def __init__(self, builddir):
        try:
            with open(os.path.join(builddir, 'meson-info', 'intro-install_plan.json')) as f:
                self.install_plan = json.load(f)
        except OSError as e:
            raise Exception(f'ERROR: meson did not generate intro-install_plan.json: {e}') from e

        try:
            with open(os.path.join(builddir, 'meson-info', 'meson-info.json')) as f:
                self.meson_info = json.load(f)
        except OSError as e:
            raise Exception(f'ERROR: meson did not generate meson-info.json: {e}') from e

        self.handlers = {'python': self.handle_python}

    def validate(self, filename):
        """Validate that a given file is in an appropriate meson.build file."""
        for language, pattern in SRC_RES.items():
            if pattern.match(filename):
                return self.handlers[language](filename)

        # If the file is unrecognized, return True
        return True

    def handle_python(self, filename):
        """Validate python source code."""
        sourcedir = self.meson_info['directories']['source']
        if not sourcedir.endswith('/'):
            sourcedir += '/'
        if filename in [d[len(sourcedir):] for d in self.install_plan['python'].keys()]:
            return True
        return False


#
# CLI functions
#
def parse_args(arguments):
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        'Check that all source files are listed in the meson.build file.'
        )
    parser.add_argument(
        '--includes',
        '-i',
        type=str,
        action='append',
        default=[],
        help='regular expression to match source code filenames.  May be given'
        ' more than once.  The patterns are in addition to the builtin'
        ' pattern.'
        )
    parser.add_argument(
        '--excludes',
        '-e',
        type=str,
        action='append',
        default=[],
        help='regular expression patterns to exclude files as source code.'
        ' Use this if you wish to remove some of the patterns found by the'
        ' builtin pattern'
        )
    parser.add_argument(
        '--allow-tests',
        action=compat.BooleanOptionalAction,
        default=False,
        help='If specified, test files may be checked for existence in'
        ' meson.build files as well.  When unset, anything in a subdirectory'
        ' named `tests` or `test` is skipped.  Note that the filenames still'
        ' have to match something in --include.  The default is not to check'
        ' test files.'
        )
    parser.add_argument('filenames', nargs='*', help='list of files to check', default=[])
    args = parser.parse_args(arguments)

    return args


def _include_source(filename, includes):
    if DEFAULT_INCLUDE_RE.match(filename):
        return True

    for include in includes:
        if re.match(include, filename):
            return True

    return False


def _exclude_source(filename, excludes, allow_tests=False):
    if not allow_tests:
        if TEST_RE.match(filename):
            return True

    for exclude in excludes:
        if re.match(exclude, filename):
            return True
    return False


def filter_on_source(filenames, allow_tests, includes=(), excludes=()):
    """Filter a list of filenames for those that we think are source code."""
    possibly_source = (f for f in filenames if _include_source(f, includes))
    return [f for f in possibly_source if not _exclude_source(f, excludes, allow_tests)]


def main() -> int:
    """Run meson-file-list."""
    args = parse_args(sys.argv[1:])

    # Only process source code files
    src_files = filter_on_source(args.filenames, args.allow_tests, args.includes, args.excludes)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a meson builddir which has the information we need
        try:
            subprocess.check_call(['meson', tmpdir], shell=False)
        except subprocess.CalledProcessError as e:
            print(f'ERROR calling meson: {e}')
            return 2

        validator = Validator(tmpdir)
        errors = False
        for filename in src_files:
            if not validator.validate(filename):
                print(f'ERROR: {filename} was not included in a meson.build file')
                errors = True

        if errors:
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
