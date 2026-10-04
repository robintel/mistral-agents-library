# C dialect

Baseline style for C work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Eras

The build flag names the era: C89/C90 (declarations at block top,
`/* */` comments only), C99 (mixed declarations, `//`, stdint, VLAs),
C11 (threads, `_Generic`), C17, C23. Write the era `-std=` names; a
standard bump is its own brief.

## Idiom

- const-correctness: pointers that do not modify take const.
- Fixed-width types for storage and wire formats: `uint32_t` over
  `unsigned long`; plain `int` only for local arithmetic.
- Ownership stated by convention — who allocates, who frees — written
  where the function is declared.

## Structure

- One header per module; the header is the public API. `static` is
  the default; non-static is a decision.
- Include guards or `#pragma once` per the repo; includes minimal.

## Errors

- Every malloc and every syscall checked; failure handled or
  explicitly annotated as impossible.
- errno read immediately after the failing call.
- Cleanup paths: `goto cleanup` is idiomatic C — forward-only, once
  per function.

## Testing

- The repo's framework; pure modules stay pure so they stay testable.

## Dependencies

- System libraries linked explicitly; vendored code pinned by commit.

## Starting from scratch

CMake or plain Makefiles per the brief's scale; `-Wall -Wextra
-Werror` from day one; sanitizers in the test build.

## Pitfalls

- `strncpy` does not null-terminate; the trap is famous for a reason.
- Signed/unsigned comparison traps in loops.
- `strlen` on untrusted input as a bound.
- Undefined behavior treated as "works here": aliasing violations,
  shifts past width, sequence-point assumptions.
