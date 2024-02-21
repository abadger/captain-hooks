# Captain Hooks

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/abadger/captain-hooks/main.svg)](https://results.pre-commit.ci/latest/github/abadger/captain-hooks/main)
[![Coverage](https://github.com/abadger/captain-hooks/actions/workflows/coverage.yml/badge.svg)](https://github.com/abadger/captain-hooks/actions/workflows/coverage.yml)
[![codecov](https://codecov.io/gh/abadger/captain-hooks/branch/main/graph/badge.svg?token=GD9HJBEQSM)](https://codecov.io/gh/abadger/captain-hooks)
[![Code Scanning - Action](https://github.com/abadger/captain-hooks/actions/workflows/codeql.yml/badge.svg)](https://github.com/abadger/captain-hooks/actions/workflows/codeql.yml)

Collection of pre-commit hooks

<!-- TOC -->

## Usage

You can use hooks from this repository to your code by adding the following to
your `.pre-commit-config.yaml` file:

``` yaml
- repo: https://github.com/abadger/captain-hooks
  rev: 0.2.0  # Update using: pre-commit autoupdate --repo https://github.com/abadger/captain-hooks
  hooks:
  - id: meson-file-list
  # [...]
```

## Provided hooks

- meson-file-list: Ensure that meson.build files contain all of the source code files.
