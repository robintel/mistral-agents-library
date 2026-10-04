# Ruby dialect

Baseline style for Ruby work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from
scratch section supplies the defaults.

## Eras

The 2/3 boundary is the practical marker: 3.0 separated positional
from keyword arguments, and 2.7 warned first — calls written for 2.x
may be wrong on 3.x. Frozen string literals opt in by magic comment
per file. The Gemfile's `ruby` directive names the floor; write the
era you find.

## Idiom

- Blocks over explicit iterator objects; each/map/select read best.
- Frozen string literals magic comment on new files.
- No monkey patching of core classes; refinements only where the
  need is real, never silent reopening.
- Struct for value objects; OpenStruct is slow magic, never in new
  code.

## Structure

- Modules namespaced; one class per file named for it.
- attr_reader over hand-written getters; visibility explicit where it
  matters.

## Errors

- Specific exception classes; rescue StandardError's subclasses,
  never Exception itself.
- fail early with messages carrying context; retry only with backoff.

## Testing

- RSpec or Minitest per the repo.

## Dependencies

- Gemfile pins; add none without a stated reason.

## Starting from scratch

Ruby 3.x, Bundler, RSpec, RuboCop with a pinned config.

## Pitfalls

- Default arguments evaluated once — mutation through them persists.
- `==`, `equal?`, `eql?` mean different things; know which.
- Implicit `to_s` on nil hiding null bugs.
- Symbols built from untrusted input — an unbounded, never-freed
  table.
