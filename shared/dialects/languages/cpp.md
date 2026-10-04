# C++ dialect

Baseline style for C++ work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Eras

C++ eras are named by the standard flag, and they are vast: 98/03,
11 (auto, lambdas, move semantics, smart pointers), 14, 17 (structured
bindings, optional/variant/string_view), 20 (concepts, ranges,
coroutines), 23. The build names the standard; write its idiom. A
standard bump is a migration brief — one of the biggest in the
industry.

## Idiom

- RAII for every resource; `new`/`delete` never appear in new code —
  make_unique/make_shared and containers own.
- Rule of zero: a class manages no resources, or is a dedicated
  owner; the rule of five only for owners.
- const-correctness everywhere; noexcept where the guarantee holds.
- `auto` where the right side states the type; explicit types at API
  boundaries.

## Structure

- The header is the contract; the implementation split per repo
  convention.
- Modules (C++20) only where the build and repo already use them.

## Errors

- Exceptions per the repo's policy — enabled or `-fno-exceptions`,
  both legitimate, mixing is not.
- Expected-shaped types (23) or the repo's outcome type where errors
  are expected values.

## Testing

- The repo's framework; Catch2 or gtest by repo convention.

## Dependencies

- Conan/vcpkg or system packages pinned; add none without a reason.

## Starting from scratch

CMake, C++20 unless the brief says otherwise, tests from the first
file, sanitizers in the test build.

## Pitfalls

- Dangling references: views and spans never own.
- Lambdas capturing references that outlive the frame.
- Hidden virtual calls in constructors; slicing by value assignment.
- Iteration invalidation: mutate-while-iterating on containers.
