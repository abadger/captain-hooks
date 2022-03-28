# Copyright: (c) 2022, Toshio Kuratomi <a.badger@gmail.com>
# License: AGPL-3.0-or-later
"""
Compatibility code for different python3 versions.

The minimum Python 3 version is 3.6.  This file includes compatibility when we
make use of newer features.
"""

try:
    from argparse import BooleanOptionalAction  # type: ignore[attr-defined]
except ImportError:
    from .vendored._argparse import BooleanOptionalAction  # type: ignore[no-redef,misc]

__all__ = ('BooleanOptionalAction', )
