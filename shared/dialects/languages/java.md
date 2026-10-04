# Java dialect

Baseline style for Java work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Eras

Java idiom is era-specific, and the build names the era: the pom or
gradle target release decides what you write. 8 (lambdas, streams,
Optional; `javax.*`), 10 (`var`), 17 (records, sealed types, switch
expressions), 21 (virtual threads, pattern matching for switch,
sequenced collections). Write the era you find — modernizing the
language level is its own brief with its own plan, never a ride-along.

## Idiom

- One public top-level class per file; the file names it.
- Streams for transformations, not for ceremony: a loop that reads
  clearer is not a defect.
- Optional as a return type; never a field or a parameter.
- `var` where the right side states the type, never where it hides.

## Structure

- Records (17+) for value objects; for older eras, equals/hashCode
  done once, or the repo's builder library.
- Interfaces small; implementations never leak through return types.

## Errors

- Specific exceptions with context; never catch-and-swallow, never
  `Exception` where a specific type exists.
- try-with-resources for everything AutoCloseable.
- Checked exceptions follow the repo's policy — documented or wrapped
  with the cause preserved.

## Testing

- JUnit as the repo pins it — 4 or 5 is era again; assertion library
  the repo already uses, not a new one.

## Dependencies

- The build file pins; add none without a stated reason. `javax` vs
  `jakarta` follows the era — never mixed.

## Starting from scratch

When no conventions exist: Maven, JUnit 5, Java 21, unless the brief
says otherwise.

## Pitfalls

- Mutable static state — the hidden global.
- `==` on boxed types; `equals` for strings and objects.
- `SimpleDateFormat` shared across threads; java.time is immutable —
  use it.
- Finally blocks that throw, losing the original exception.
- Stream collectors that hide nulls.
