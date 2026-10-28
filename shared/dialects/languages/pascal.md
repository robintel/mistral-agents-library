# Pascal dialect

**Status: experimental and conservation** — never validated against
a production Pascal estate; findings get practitioner review.

A conservation contract, not an idiom floor. Pascal in production runs
Turbo Pascal (DOS, the 3.0–7.0 era), Delphi (Windows, the OOP
extension), or Free Pascal (modern, cross-platform). The running
system is the spec; the regression baseline is captured before any
change.

## Eras

Three eras, three disciplines: Turbo Pascal (procedural, DOS, units
as modules, TP 3.0–7.0), Delphi (Object Pascal, VCL/FMX, Windows
and cross-platform, Delphi 1 through 12), and Free Pascal (modern
OSS, Lazarus IDE, compiles Turbo Pascal and Delphi code). The build
names the era: `.dpr`/`.dpk` for Delphi, `.lpr`/`.pp` for Free
Pascal, `.tpu` units for Turbo Pascal. Match the era of the file.

## Preservation over modernization

- Match the existing style absolutely: `begin`/`end` blocks,
  PascalCase versus camelCase (the file's convention wins),
  `with` statements (common in Delphi-era code — do not refactor
  them silently, they are load-bearing for readability).
- Strong typing is the language's contract: do not weaken it with
  `Variant` (Delphi) or `untyped` (FPC) to make a change easier.
- `const` sections and typed constants are the configuration
  surface; changing a constant changes behavior everywhere it
  is referenced.

## Structure

- Units (Turbo Pascal/FPC) or `unit`/`interface`/`implementation`
  (Delphi): one unit per file, named for it. The interface section
  is the public API; the implementation section is private.
- `uses` clause in the interface for public dependencies, in the
  implementation for private ones. Circular `uses` in interface
  sections are a design error.
- OOP in Delphi/FPC: classes in `type` blocks, `published` for
  RTTI (designer-visible), `private`/`public` for the rest.
  Constructors named `Create`, destructors `Destroy`, `FreeAndNil`
  for safe cleanup.

## Errors

- Delphi/FPC: `try...except` with specific exception classes;
  `raise` with context. Turbo Pascal: `{$I-}` for I/O error
  checking, `IOResult` — the old error model.
- `SysUtils.Exception` is the base; catch specific types, never
  bare `except` without a handler.
- FPC: `try...finally` for cleanup, `try...except` for handling.

## Testing

- Delphi: DUnitX. FPC: FPCUnit. Turbo Pascal: no standard
  framework — the regression baseline is program output on known
  inputs.
- Old Pascal rarely has tests: capture stdout/file output before
  changing, diff after.

## Pitfalls

- `with` statements: convenient, dangerous. `with` chains
  (`with A, B do`) silently change meaning when fields share
  names.
- Short-circuit evaluation: `{$B-}` (Turbo Pascal) is the
  default — `if (A <> nil) and (A.Field = x)` crashes on nil.
  Delphi/FPC default to complete evaluation; match the file's
  compiler directives.
- String types: Turbo Pascal `String` is `ShortString` (255
  chars max) unless `{$H+}` (AnsiString). Delphi `string` is
  `AnsiString` (or `UnicodeString` in Delphi 2009+). The string
  type is an era marker — changing it changes memory layout.
- Integer sizes: `Integer` is 16-bit in Turbo Pascal, 32-bit in
  Delphi/FPC. `Smallint`/`Longint` are explicit. Range overflow
  is silent in old code.
- Pointer arithmetic: `Ptr` and `^` dereference in Turbo Pascal;
  `Pointer` and `GetMem`/`FreeMem` in Delphi. Mixing allocators
  leaks.
- `case` statements without `else`: no default, falls through
  silently. Turbo Pascal `case` on strings is not allowed.
