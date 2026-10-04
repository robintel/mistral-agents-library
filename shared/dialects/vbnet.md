# VB.NET dialect

Baseline style for VB.NET work. The repo's pinned conventions win on
conflict. This dialect is VB.NET; classic Visual Basic — VB6 and
earlier — is a different language: preservation rules apply there, not
these. Match the old file absolutely and modernize nothing silently.

## Idiom

- `Option Strict On` and `Option Explicit On` for new code.
- .NET methods over the Visual Basic runtime residue: `String.Substring`
  over `Mid`, `.Length` over `Len` — `Microsoft.VisualBasic` calls are
  VB6 accent, not VB.NET idiom.
- `Try...Catch` for error handling; `On Error Resume Next` and `GoTo`
  handlers are the old language wearing new clothes.

## Structure

- Explicit types on declarations; never rely on default typing.
- `ByVal` stated, `ByRef` only when the caller must see the change.
- Properties over public fields for anything on an interface.

## Errors

- Specific exceptions with context; never catch-and-continue silently.
- `Using` blocks for everything IDisposable.

## Testing

- The repo's framework, xUnit by default for new work.

## Dependencies

- PackageReference pins; add none without a stated reason.

## Starting from scratch

When no conventions exist: prefer C# — VB.NET for new projects only
when the estate demands it, and say so in the report.

## Pitfalls

- Integer division `\` where `/` was meant.
- Late binding sneaking in with `Option Strict Off`.
- `Nothing` versus default-value comparisons; `IsNothing` versus
  `Is Nothing`.
- String comparison semantics: `Option Compare` decides Text versus
  Binary — know which the file uses.
