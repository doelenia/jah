# Contributing to Jah

Jah accepts contributions through [GitHub issues](https://github.com/doelenia/jah/issues) and [pull requests](https://github.com/doelenia/jah/pulls).

## What this repository contains

The public tree is the shared system:

- `system/` — agent protocol, bootstrap, engines, and release tooling
- `README.md`, `LICENSE`, this file, and `.github/`

A principal (`users/<id>/`) stays on your machine. Do not put principal data, credentials, or anything from `users/` in an issue or pull request.

## Issues

Open an issue for a bug, a documentation gap, or a proposal. Describe what you saw and what you expected. Leave out local principal contents and secrets.

## Pull requests

1. Fork the repository and work on a branch.
2. Keep the change inside the public tree.
3. If you change tracked public files (`system/`, `README.md`, `.gitignore`, `LICENSE`, `CONTRIBUTING.md`, or `.github/`), bump the system version before you commit:

   ```bash
   python3 system/release/scripts/bump_release.py --bump patch -m "Short summary of the change"
   python3 system/release/scripts/check_release.py
   ```

   Patch for docs and small fixes. Minor for a backward-compatible protocol or engine addition. Major for a breaking protocol or bootstrap change. Details: [system/release/versioning.md](system/release/versioning.md).

By submitting a pull request, you agree that your contribution is licensed under the [MIT License](LICENSE).

## Copyright

Copyright (c) 2026 Allen Chen. See [LICENSE](LICENSE).
