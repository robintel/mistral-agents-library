# C# dialect

Baseline style for C# work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Eras

C# idiom is era-specific, and the csproj names the era: .NET Framework
4.x (Windows-bound, older language versions) versus .NET 6/8
(file-scoped namespaces, records, pattern matching). Write the era the
target framework names — modernizing the runtime is its own brief.

## Idiom

- File-scoped namespaces in new code where the language version allows;
  block namespaces where the repo does otherwise.
- `var` where the right side states the type; explicit where it hides.
- LINQ for transformations; a loop that reads clearer is not a defect.
- `const` for compile-time, `static readonly` for runtime-once.

## Structure

- Records for value objects where the language version has them;
  classes with equality where it does not.
- Nullable reference types on for new projects; the era decides for
  old ones.

## Errors

- Specific exceptions with context; exception filters over
  catch-and-rethrow.
- `using var` for IDisposable, scoped tightly.

## Testing

- The repo's framework — xUnit by default for new work.

## Dependencies

- PackageReference pins; add none without a stated reason.

## Starting from scratch

When no conventions exist: .NET 8, xUnit, nullable on.

## Pitfalls

- `async void` — fire-and-forget that crashes the process;
  `async Task`.
- `.Result` and `.Wait()` — deadlocks and swallowed exceptions;
  await.
- `DateTime.Now` for durations — `DateTime.UtcNow` or `Stopwatch`.
- Culture-sensitive parsing in pipelines — `InvariantCulture`.
- String concatenation in hot loops.
