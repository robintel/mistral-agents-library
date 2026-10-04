# Perl dialect

Baseline style for Perl work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from
scratch section supplies the defaults.

## Eras

Two Perls in the wild: legacy (no strict, bareword filehandles,
package globals, CGI-era patterns) and modern (strict + warnings,
lexical everything, 5.36+ signatures and try/catch). The codebase
declares which. Modernizing a legacy codebase is a migration brief —
but new code gets strict regardless: the era rule is repo-wide
history, not per-file fashion.

## Idiom

- `use strict; use warnings;` — every new file, no exceptions.
- Lexical filehandles; three-argument open with the error checked.
- Variables declared at the smallest useful scope.
- No implicit `$_` in complex expressions; name the variable.

## Structure

- Packages per file named for them; package-scoped, not global.
- Explicit returns; no implicit last-expression return in nontrivial
  code.

## Errors

- `die` with context, never bare; `eval` is the exception boundary,
  `$@` checked immediately.
- autodie in new code: syscalls check themselves.

## Testing

- Test2 or Test::More per the repo; `prove` runs the suite.

## Dependencies

- cpanfile pins; add none without a stated reason.

## Starting from scratch

Perl 5.36+, strict, warnings, signatures, cpanfile, Test2.

## Pitfalls

- Context — scalar versus list — deciding meaning silently.
- `$!` read too late; unchecked opens and system calls.
- Numeric versus string comparison operators swapped: `==` against
  `eq`.
- Regular expressions without `use re '/x'` turning into line noise
  past one line.
