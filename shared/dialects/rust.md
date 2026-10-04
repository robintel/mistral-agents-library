# Rust dialect

Baseline style for Rust work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Idiom

- rustfmt output; clippy clean, not clippy silenced.
- `Result` over panics: `unwrap`/`expect` only in tests, and `expect` only
  with a message that explains the invariant.
- Cloning to appease the borrow checker is allowed once, with a comment
  saying why the clone is cheaper than the restructure.

## Structure

- Traits for abstraction the caller needs, not for imagined futures.
- `pub` is the public contract; everything else stays private by default.

## Errors

- `?` for propagation; concrete error types (`thiserror`-shaped) in
  libraries, aggregated errors (`anyhow`-shaped) in binaries — matching
  what the repo already does.

## Testing

- `#[cfg(test)]` unit tests beside the code; integration tests in
  `tests/`; property tests only where the contract is genuinely numeric.

## Dependencies

- `Cargo.toml` pins with `^` ranges; add none without a stated reason.

## Starting from scratch

When no repo conventions exist yet, these are the pins:

- `cargo init`; rustfmt and clippy as shipped; `#[cfg(test)]` from the
  first module; dependencies only as the brief demands.

## Pitfalls

- Blocking calls inside async contexts — `tokio::task::spawn_blocking`.
- Indexing panics: `get()` when the bounds are not proven.
- `as` casts truncate silently; use `try_from`.
- Mutex guard held across an await; `await` on a lock — use async-aware
  primitives.
