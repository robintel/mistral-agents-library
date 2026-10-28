# BASIC dialect

**Status: experimental and conservation** — never validated against
a production BASIC estate; findings get practitioner review.

A conservation contract, not an idiom floor. BASIC in production is
line-numbered (GW-BASIC, BASICA, QBasic's unstructured mode) or
structured (QBasic, QuickBASIC, VB6-era). The running system is
the spec; the regression baseline is captured before any change.

## Eras

Three eras, different disciplines: line-numbered BASIC (GW-BASIC,
BASICA on DOS, every line has a number, `GOTO` is the control
flow), structured BASIC (QBasic/QuickBASIC, `SUB`/`FUNCTION`,
no line numbers required, compiled), and the visual era (VB6's
BASIC engine, event-driven, forms as code). The file declares its
era: line numbers mean line-numbered; `SUB`/`FUNCTION` without
line numbers means QBasic/QuickBASIC. Match the file.

## Preservation over modernization

- Line numbers are the addressing system: `GOTO 1000`, `GOSUB
  2000`, `ON ERROR GOTO 500`. Renumbering is a migration brief,
  not a cleanup. `RENUM` changes every reference — verify all of
  them.
- Global state is the default: every variable is global unless
  declared `LOCAL` (QBasic) or `Dim` inside a `SUB`. The data
  flow is implicit and cross-procedural. Trace it before changing
  it.
- `OPTION BASE 0` versus `OPTION BASE 1`: the array indexing
  floor is a program-wide setting, stated once, not inherited.
  Changing it shifts every array.

## Data honesty

- Type suffixes decide precision: `X%` is integer, `X!` is
  single, `X#` is double, `X$` is string. A variable's suffix is
  its type — adding a suffix where none existed changes the
  variable, silently.
- `DEFINT A-Z` (default integer) in old code: variables without
  suffixes are integers, not floats. The default type is a
  program-wide setting.
- String length: old BASIC strings are fixed-length or
  variable up to 255 chars (`DIM X$ AS STRING * 80` is VB, not
  QBasic). QBasic `STRING` is variable-length up to 32K.

## Structure

- Line-numbered: `GOSUB`/`RETURN` for subroutines, `ON n GOSUB`
  for dispatch. No recursion (stack overflow on old interpreters).
- QBasic/QuickBASIC: `SUB`/`FUNCTION` with `DECLARE`, `DIM
  SHARED` for globals, `TYPE` for records. Modules (`.BAS`) are
  separate compilation units.
- No namespaces, no packages: every name is global. Name
  collisions are silent overwrites.

## Errors

- `ON ERROR GOTO <line>`: the error handler is a labeled block,
  not a catch clause. `ERR` is the error code, `ERL` is the
  line where it occurred.
- `RESUME`, `RESUME NEXT`, `RESUME <line>`: the error recovery
  verbs. `RESUME NEXT` skips the failing statement — the silent
  failure mode of old BASIC.
- No structured exceptions. The error handler must be installed
  before the code that can fail, and every `GOTO` out of it must
  `RESUME` or the handler stays active.

## Testing

Old BASIC rarely has tests. The regression baseline is program
output on known inputs — screen output, file dumps, printed
reports. Capture before changing, diff after.

## Pitfalls

- `GOTO` spaghetti: the control flow is the program. Understand
  the graph before touching any node.
- Implicit type declarations: `FOR I = 1 TO 10` makes `I` an
  integer (via `DEFINT`), but `FOR X = 1.5 TO 10` makes `X`
  a float. The loop variable's type comes from the literal.
- Integer overflow: `X%` wraps at 32767 (signed 16-bit). No
  error, silent wraparound.
- `PRINT USING` formats: the format string decides output
  precision. Changing the format changes the output contract.
- `DATA`/`READ`/`RESTORE`: the inline data mechanism. `RESTORE
  <line>` resets the read pointer — shared state across the
  program.
- Floating-point comparison: `IF X = 0.1 + 0.2 THEN` is false
  (0.30000000000000004). Old BASIC has no epsilon culture;
  rounding is explicit.
