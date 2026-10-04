# Go dialect

Baseline style for Go work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Idiom

- gofmt output is non-negotiable; no cleverness the formatter did not ask
  for.
- MixedCase names, no underscores; acronyms all caps (`HTTPServer`).
- Accept interfaces, return structs; define interfaces where they are
  consumed, not implemented.

## Structure

- `cmd/` for binaries, `internal/` for anything not importable outside the
  module; no `pkg/` unless the repo already has one.
- No magic in `init()`: explicit calls beat invisible ones.

## Errors

- `error` is the last return value; wrap with `%w`; panics never for
  expected failures.
- `context.Context` is the first parameter of anything that can block;
  cancellation is honored all the way down.

## Testing

- Table-driven tests; `t.Parallel()` where the code under test is safe.

## Dependencies

- `go.mod` and `go.sum` are the pin; add none without a stated reason.

## Starting from scratch

When no repo conventions exist yet, these are the pins:

- `go mod init`; `cmd/<binary>/` + `internal/` layout; standard library
  testing, table-driven from the first test; gofmt as shipped.

## Pitfalls

- Goroutine leaks: every goroutine exits via context, channel, or errgroup.
- Loop variable capture on Go before 1.22.
- Slice aliasing: `append` may share the backing array.
- Write to a nil map; `defer` inside loops; `time.After` in loops leaks.
