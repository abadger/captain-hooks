# This is a copy of BooleanOptionalAction from the Python-3.9 code.
# https://github.com/python/cpython/blob/41b223d29cdfeb1f222c12c3abaccc3bc128f5e7/Lib/argparse.py#L856
# It is licensed under the Python Software Foundation License:
# https://github.com/python/cpython/blob/main/LICENSE
#
# The intention is that this is used from captain_hooks.compat.BooleanOptionalAction rather than
# from this file. That way we use the version in the python stdlib if it is available and use this
# code if it is not.
"""Backport of BooleanOptionalArgs from Python-3.10."""
from argparse import Action
from argparse import SUPPRESS

# Vendored code so ignore all of these
# pylint:disable=missing-class-docstring,redefined-builtin,too-many-arguments


class BooleanOptionalAction(Action):

    def __init__(self,
                 option_strings,
                 dest,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):

        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)

            if option_string.startswith('--'):
                option_string = '--no-' + option_string[2:]
                _option_strings.append(option_string)

        if help is not None and default is not None and default is not SUPPRESS:
            help += ' (default: %(default)s)'

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, not option_string.startswith('--no-'))

    def format_usage(self):
        return ' | '.join(self.option_strings)
