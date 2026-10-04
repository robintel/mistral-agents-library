# TypeScript dialect

Baseline style for TypeScript work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Idiom

- Strict mode; `unknown` over `any`; no non-null assertions (`!`) in
  library code.
- `===` always; async/await over raw promise chains.

## Structure

- Interfaces or type aliases for shapes; discriminated unions over
  optional-field soup — a union member names its case.
- One export per module surface: the public API is what `index.ts` ships.

## Errors

- Error subclasses carrying context; never throw strings or plain objects.
- Expected failures return typed results when the caller must branch;
  exceptions are for the exceptional.

## Testing

- The repo's framework (vitest, jest); no snapshot tests for logic.

## Dependencies

- Pinned by the lockfile; add none without a stated reason in the report.

## Starting from scratch

When no repo conventions exist yet, these are the pins:

- Strict `tsconfig` (`strict`, `noUncheckedIndexedAccess`); ESM modules;
  the framework named in the brief; vitest for tests.

## Pitfalls

- Floating promises — every await or explicit `.catch`.
- `sort()`, `splice()`, `reverse()` mutate in place; copy first.
- Date timezone math as strings — use the library the repo already pins.
- Unbounded `any` leaking in from untyped third-party boundaries: type the
  boundary once.
