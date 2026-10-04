# JavaScript dialect

Baseline style for JavaScript work. The repo's pinned conventions
win on conflict; when the repo is empty or silent, the Starting from
scratch section supplies the defaults. TypeScript has its own
dialect — this one is the untyped language.

## Eras

JavaScript eras are sharp: ES5 (var, callbacks), ES2015 (let/const,
classes, modules, Promises), the module era — CommonJS versus ESM,
named by package.json `"type"` — and ES2020 (nullish coalescing,
optional chaining). The build names the era; write its idiom. A
callbacks -> promises -> async/await migration is its own brief,
never a ride-along.

## Idiom

- `const` by default, `let` only when reassigned; `var` never in
  modern code, everywhere in ES5 code.
- `===` always; truthiness checks only where intentional.
- async/await in modern code; callbacks only in ES5 code.
- Destructuring and spread over manual property copying.

## Structure

- Modules per the package.json type; one export per file where it
  reads clearly.
- Functions and closures first; a class only when it carries state
  and polymorphism.

## Errors

- Every promise awaited or explicitly handled — floating promises
  are the classic leak.
- Errors carry context; rethrow with `cause` where the runtime
  supports it.

## Testing

- The repo's framework — vitest, jest, or node:test; introduce none
  new.

## Dependencies

- Lockfile pinned; add none without a stated reason.

## Starting from scratch

ESM (`"type": "module"`), Node LTS, vitest, unless the brief says
otherwise.

## Pitfalls

- `this` losing its receiver when a method is extracted.
- Sort mutating in place when a copy was meant.
- `typeof null === 'object'`; `Array.isArray` for arrays.
- String plus number coercion; `==` across types.
