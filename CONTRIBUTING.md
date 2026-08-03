# Contributing to Daisy

Thank you for your interest in Daisy. The project is currently maintained as a
personal software and learning project. Contributions are considered at the
repository owner's discretion.

## Before starting

For bugs and small improvements, open an issue first. For larger gameplay,
story, architecture, or data-model changes, discuss the approach before writing
code. This avoids work that conflicts with the project's direction.

## Local setup

Requires Python 3.10 or newer.

```bash
python -m pip install ".[dev]"
```

Run the project checks before submitting a pull request:

```bash
ruff check daisy tests run_game.py run_gui.py
ruff format --check daisy tests run_game.py run_gui.py
python -m compileall -q daisy run_game.py run_gui.py
python -m pytest
```

To apply the formatter locally:

```bash
ruff format daisy tests run_game.py run_gui.py
```

## Pull requests

- Keep each pull request focused on one change.
- Explain the motivation and visible effect.
- Add or update tests when behaviour changes.
- Update documentation when commands, data, or gameplay change.
- Do not include unrelated formatting or generated files.

## Ownership and usage rights

Submitting a contribution does not grant permission to reuse or redistribute
the project. By submitting a pull request, you confirm that you created the
contribution and permit the repository owner to use, modify, and include it in
Daisy under the project's existing proprietary terms. See [LICENSE.md](LICENSE.md).
