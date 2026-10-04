# PHP dialect

Baseline style for PHP work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from
scratch section supplies the defaults.

## Eras

PHP eras are sharp: 5 (OOP arrives), 7 (scalar type hints, return
types, `declare(strict_types=1)`), 8 (constructor promotion, match,
readonly), 8.1+ (enums, fibers) — plus the dark age before Composer.
composer.json names the era; write its idiom.

## Idiom

- `declare(strict_types=1)` and full type signatures in all 7+ code.
- Null coalescing and null-safe operators over isset chains.
- `match` (8) over `switch` where it reads clearer.
- Array functions over manual loops where they read clearer.

## Structure

- Namespaces matching paths; one class per file named for it.
- Constructor promotion (8) for value-heavy classes; readonly (8.1)
  for value objects.
- No mixed HTML/code files in new code — templates separate.

## Errors

- Exceptions over return-false-plus-error-string; never suppress with
  `@`.
- Specific exception subclasses carrying context.

## Testing

- PHPUnit or Pest per the repo.

## Dependencies

- composer.lock committed; add none without a stated reason.

## Starting from scratch

PHP 8.2+, strict_types on, Composer, PHPUnit, enums for closed sets.

## Pitfalls

- Loose comparison surprises: `==` between 0 and strings.
- Array auto-vivification: writing to an undefined index creates it.
- `in_array` without the strict flag matching loosely.
- Null sneaking past a type declaration in pre-strict_types code.
