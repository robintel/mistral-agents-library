# Python dialect

Baseline style for Python work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Idiom

- PEP 8. If the repo pins a formatter or linter (ruff, black), its word is
  law.
- Type hints on every public function.
- f-strings for interpolation; `pathlib` over `os.path` string surgery.

## Structure

- One responsibility per module; `__init__.py` re-exports the public
  surface and nothing else.
- Dataclasses (or the repo's model library) for value objects; no bare
  dicts crossing module boundaries.

## Errors

- Raise specific exceptions; never bare `except:`.
- Resources through context managers; no manual `close`.

## Testing

- pytest; fixtures named after what they provide; no test-order
  dependencies.

## Dependencies

- Pinned in `pyproject.toml` or `requirements.txt`; add none without a
  stated reason in the report.

## Starting from scratch

When no repo conventions exist yet, these are the pins:

- `pyproject.toml`; src layout (`src/<package>/`); ruff for format and
  lint; pytest; type hints from the first file.

## Pitfalls

- Mutable default arguments; late-binding closures.
- `time.time()` for durations — use `time.monotonic()`.
- Naive datetimes: attach a timezone (`zoneinfo`), always.
- `is` where `==` belongs; shadowing stdlib names (`type`, `id`).
