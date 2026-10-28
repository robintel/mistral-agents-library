# Visual Basic dialect (classic, VB6 and earlier)

**Status: experimental and conservation** — never validated against
a production VB6 estate; findings get practitioner review. This
contract is classic Visual Basic (VB6 and earlier). VB.NET is a
different language — see `vbnet.md` for that dialect.

A conservation contract, not an idiom floor. Classic VB in production
is event-driven, COM-based, and tightly coupled to the Windows API
and Office VBA. The running system is the spec; the regression
baseline is captured before any change.

## Eras

VB6 (1998, the last classic version, COM-based, Windows-only) and
VBA (the Office-hosted variant, still shipping in Excel/Access
workbooks). VB6 and VBA share the language but not the runtime:
VB6 compiles to native code; VBA runs in the Office host. The
project file (`.vbp`/`.vba`) names the era. Match the file.

## Preservation over modernization

- `On Error Resume Next` is the error handling of the era: it
  suppresses errors and continues. Removing it changes behavior
  everywhere — every line after it may have been silently failing.
  Understand what it hides before touching it.
- Global state is structural: module-level `Public` variables,
  `Global` in `.bas` modules, form-level state that persists
  across calls. The data flow is implicit and cross-form.
- Forms are code and UI in one file (`.frm`): the layout is the
  designer's, the logic is the code's, and both live in the same
  artifact. Changing one can break the other.

## Structure

- Modules (`.bas`) for procedures, class modules (`.cls`) for
  objects, forms (`.frm`) for UI + logic. No namespaces —
  every public name is global across the project.
- COM is the component model: `CreateObject`, `GetObject`,
  early-bound (`Dim x As New Foo`) versus late-bound (`Dim x As
  Object`). Early binding is compile-time checked; late binding
  (`As Object`) defers everything to runtime.
- Event-driven: `Sub Button_Click()`, `Sub Form_Load()` —
  the runtime calls the handler, not your code.

## Data honesty

- Type suffixes: `X%` integer, `X&` long, `X!` single, `X#`
  double, `X$` string, `X@` currency. `Dim X As String` is the
  explicit form; the suffix is the inline form. Both exist in
  old code — match the file.
- `Variant` is the untyped container: it holds anything, and
  `IsNumeric`, `IsDate`, `VarType` are the runtime type checks.
  `Variant` arithmetic coerces silently — `"1" + 2` is `3`.
- Arrays: `Dim arr(1 To 10)` — the bounds are explicit. Default
  is `0 To n` unless `Option Base 1`.

## Errors

- `On Error GoTo <label>`: the handler is a labeled block at the
  bottom of the procedure.
- `On Error Resume Next`: suppress and continue — the most
  dangerous line in the language.
- `On Error GoTo 0`: disables the handler within the current
  procedure.
- `Err.Number`, `Err.Description`, `Err.Source`: the error
  object. `Err.Clear` resets it.
- `Exit Sub`/`Exit Function` before the error handler to avoid
  falling into it on normal exit.

## Testing

VB6 has no standard test framework in the era. VBA has none either.
The regression baseline is application behavior on known inputs —
workbook outputs, form states, file contents. Capture before
changing, diff after.

## Dependencies

- COM references in the `.vbp`: `Microsoft Excel 16.0 Object
  Library`, `Scripting.FileSystemObject`, etc. The reference
  version is pinned in the project file. Changing it changes
  the API surface — the IDE resolves it, the compiler does not
  warn on breaking changes.
- No package manager. DLLs are registered with `regsvr32`.
  Deployment is an installer or manual copy.

## Pitfalls

- `On Error Resume Next` hiding failures: every subsequent line
  runs in an unknown state.
- Late binding (`As Object`): typos in method names compile
  fine, fail at runtime with "Object doesn't support this
  property or method."
- `Variant` arithmetic coercion: string + number, date +
  number, empty + zero — all silently coerce.
- Circular form references: Form A loads Form B, Form B
  references Form A. Load order is runtime state.
- `Nothing` versus `Empty` versus `Null`: three different
  "no value" states with different semantics. `Is Nothing` only
  works on objects; `IsEmpty` on Variants; `IsNull` on database
  fields.
- Integer division `\` versus float division `/`: `5 \ 2` is
  `2`, `5 / 2` is `2.5`. The operator is the type.
- String comparison: `Option Compare Binary` (default,
  case-sensitive) versus `Option Compare Text` (case-insensitive,
  locale-dependent). The setting is module-level.
- Memory: `Set x = Nothing` releases the reference, not the
  object. Circular references leak; VB6 has no garbage collector.
