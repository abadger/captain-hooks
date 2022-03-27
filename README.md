# Captain Hooks

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/abadger/captain_hooks/main.svg)](https://results.pre-commit.ci/latest/github/abadger/captain_hooks/main)
[![Coverage](https://github.com/abadger/captain_hooks/actions/workflows/coverage.yml/badge.svg)](https://github.com/abadger/captain_hooks/actions/workflows/coverage.yml)
[![codecov](https://codecov.io/gh/abadger/captain_hooks/branch/main/graph/badge.svg?token=GD9HJBEQSM)](https://codecov.io/gh/abadger/captain_hooks)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/abadger/captain_hooks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/abadger/captain_hooks/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/abadger/captain_hooks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/abadger/captain_hooks/context:python)
[![Code Scanning - Action](https://github.com/abadger/captain_hooks/actions/workflows/codeql.yml/badge.svg)](https://github.com/abadger/captain_hooks/actions/workflows/codeql.yml)

Collection of pre-commit hooks

<!-- TOC -->

## Usage

You can use hooks from this repository to your code by adding the following to
your `.pre-commit-config.yaml` file:

``` yaml
- repo: https://github.com/abadger/captain_hooks
  rev: main  # Or use the ref you want to point at
  hooks:
  - id: meson-file-list
  # [...]
```

## Provided hooks

- meson-file-list: Ensure that meson.build files contain all of the source code files.
