---
name: ma-design-principles
description: "Apply code-level design principles and defensive programming — SOLID, DRY, KISS, YAGNI, Law of Demeter, Tell Don't Ask, composition over inheritance, fail-fast validation, and defensive copying. Invoke when writing or reviewing code, when refactoring toward better design, or when you need a practical guide to principled code that complements the architecture-validator's system-level checks"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Design Principles

You are the design-principles agent. The user invoked
`/ma-design-principles`, optionally with a scope: a file, a
module, a code review, or a refactoring task. No scope means
the current project's code.

This skill covers **code-level** design principles — how to
write individual functions, classes, and modules well. It
complements the `architecture-validator` agent, which checks
the same principles at the **system** level (components,
services, layers). When the validator flags a violation, this
skill is how you fix it.

## SOLID

Five principles for object-oriented design, introduced by
Robert C. Martin (2000 paper, 2002 book). The acronym was
coined later by Michael Feathers.

### S — Single Responsibility Principle

> A class/module/function should have one reason to change.

One job. One purpose. If you can describe it with "and" —
"it validates input **and** sends email" — it has two jobs.

```python
# Bad: one class does validation, persistence, and notification.
class Order:
    def validate(self): ...
    def save_to_db(self): ...
    def send_confirmation_email(self): ...

# Good: each class has one reason to change.
class OrderValidator:
    def validate(self, order): ...

class OrderRepository:
    def save(self, order): ...

class OrderNotifier:
    def send_confirmation(self, order): ...
```

**At the function level:** a function that calculates a total
should not also print it, send it, and log it. Return the
value; let the caller decide what to do with it.

**How to check:** ask "what would make me change this?" If
the answer has multiple unrelated reasons, split it.

### O — Open/Closed Principle

> Open for extension, closed for modification.

Add new behavior by extending, not by editing existing code.

```python
# Bad: adding a new payment method requires editing this function.
def process_payment(amount, method):
    if method == "credit_card":
        ...
    elif method == "paypal":
        ...
    elif method == "crypto":  # you edited existing code
        ...

# Good: new payment methods are new classes; existing code is untouched.
class PaymentProcessor(Protocol):
    def process(self, amount: float) -> Receipt: ...

class CreditCardProcessor:
    def process(self, amount): ...

class PayPalProcessor:
    def process(self, amount): ...

class CryptoProcessor:  # extension, not modification
    def process(self, amount): ...
```

**When to bend it:** if the "extension" is a one-line `elif`
branch, a strategy pattern is over-engineering. Use the Rule
of Three (below) to decide.

### L — Liskov Substitution Principle

> Subtypes must be substitutable for their base types without
> changing correctness.

If `B` extends `A`, you should be able to use `B` anywhere you
use `A` — and the program should still be correct.

```python
# Bad: Square extends Rectangle, but set_width breaks the contract.
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w): self.width = self.height = w
    def set_height(self, h): self.width = self.height = h

# A Square is NOT a Rectangle under this contract:
# rect.set_width(5); rect.set_height(3); assert rect.area() == 15
# works for Rectangle, breaks for Square (area == 9).

# Good: don't force an inheritance relationship that violates
# the contract. Use composition or a shared interface.
```

**How to check:** if a subclass overrides a method to throw
"not supported" or to do something the parent's contract
doesn't promise, the hierarchy is wrong.

### I — Interface Segregation Principle

> Clients should not be forced to depend on methods they do
> not use.

Split fat interfaces into small, focused ones.

```python
# Bad: one interface forces implementers to provide everything.
class Worker(Protocol):
    def work(self): ...
    def eat(self): ...
    def sleep(self): ...

class Robot(Worker):  # forced to implement eat/sleep
    def work(self): ...
    def eat(self): raise NotImplementedError
    def sleep(self): raise NotImplementedError

# Good: segregated interfaces.
class Workable(Protocol):
    def work(self): ...

class Eatable(Protocol):
    def eat(self): ...

class Human(Workable, Eatable):
    def work(self): ...
    def eat(self): ...

class Robot(Workable):  # only what it needs
    def work(self): ...
```

### D — Dependency Inversion Principle

> Depend on abstractions, not concretions. High-level modules
> should not depend on low-level modules; both should depend
> on abstractions.

```python
# Bad: high-level business logic depends on a concrete database.
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()  # concrete dependency

    def place_order(self, order):
        self.db.insert(order)

# Good: depends on an abstraction.
class OrderRepository(Protocol):
    def insert(self, order): ...

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo  # injected abstraction

    def place_order(self, order):
        self.repo.insert(order)

# Wiring happens at the composition root:
service = OrderService(PostgresOrderRepository())
```

**This is the same as seam-based dependency injection** from
`/ma-legacy-testing` — the seam is the abstraction.

## Defensive Programming

Defensive programming assumes the caller is wrong until proven
right. It does not trust inputs, and it fails loudly when
assumptions are violated.

### Fail fast

Validate at the boundary. The closer to the input source, the
better. Do not let bad data propagate deep into the system.

```python
# Bad: bad input propagates; the error surfaces far from the cause.
def calculate_discount(price, percent):
    return price * (1 - percent / 100)

# Good: fail fast at the boundary.
def calculate_discount(price, percent):
    if price < 0:
        raise ValueError(f"price must be non-negative, got {price}")
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be 0-100, got {percent}")
    return price * (1 - percent / 100)
```

### Input validation

Validate at every trust boundary: function parameters, API
inputs, file reads, environment variables, database query
results. Validate type, range, format, and invariants.

| What to validate | How |
|---|---|
| Type | `isinstance(x, int)`, type hints + mypy/pyright |
| Range | `0 <= x <= 100`, explicit bounds check |
| Format | Regex, parser, schema validation (Pydantic, JSON Schema) |
| Invariants | Assertions: `assert len(items) > 0` |
| Nullability | Explicit `None` checks, not implicit truthiness |

### Assertions

Assertions document and enforce invariants — conditions that
must be true if the code is correct. They are not error
handling; they are bug detectors.

```python
# Good: assertion documents an invariant.
def binary_search(sorted_list, target):
    assert all(sorted_list[i] <= sorted_list[i+1]
               for i in range(len(sorted_list)-1)), \
        "binary_search requires a sorted list"
    ...

# Bad: using assert for input validation (stripped with -O).
def process(data):
    assert data is not None  # stripped in production!
    ...

# Use explicit validation for inputs, assertions for invariants.
def process(data):
    if data is None:
        raise ValueError("data must not be None")
    assert data.is_valid(), "invariant: data must be valid after construction"
    ...
```

**Rule:** assertions for invariants (your code's assumptions),
exceptions for input validation (the caller's contract).

### Defensive copying

Do not let mutable state leak in or out. If you receive a
mutable object, copy it if you need to modify it. If you
return one, copy it if the caller might modify it.

```python
# Bad: caller's list is mutated; internal state leaks.
class ShoppingCart:
    def __init__(self, items):
        self.items = items  # alias, not copy

    def get_items(self):
        return self.items  # caller can mutate internal state

# Good: defensive copies at the boundary.
class ShoppingCart:
    def __init__(self, items):
        self.items = list(items)  # copy on the way in

    def get_items(self):
        return list(self.items)  # copy on the way out
```

**When to skip it:** if the object is immutable (tuples,
frozensets, strings, dataclasses with `frozen=True`), copying
is unnecessary. If the object is a value type (int, float,
bool), copying is meaningless.

### Null safety

Null/nil references are the "billion-dollar mistake" (Tony
Hoare, 2009). Strategies:

| Strategy | When |
|---|---|
| **Null object pattern** | A no-op default is a valid behavior (empty list, no-op logger) |
| **Optional/Result types** | The absence is a real, handled case (Rust `Option`, Python `Optional`, Java `Optional`) |
| **Fail fast** | Null is never valid — reject at the boundary |
| **Never return null** | Return an empty collection, a default value, or throw |

```python
# Null object pattern: NullLogger does nothing, avoids null checks.
class Logger(Protocol):
    def log(self, message): ...

class RealLogger:
    def log(self, message): print(message)

class NullLogger:
    def log(self, message): pass  # no-op

# Caller never checks for null:
def process(data, logger: Logger = NullLogger()):
    logger.log("processing")  # always safe
```

### Error handling

- **Catch specific exceptions.** `except Exception` hides bugs.
- **Do not catch and continue silently.** Log, re-raise, or
  handle with a fallback — never swallow.
- **Fail at the right level.** Low-level code throws; the
  boundary (controller, CLI entry, job runner) catches and
  translates to user-facing errors.
- **Include context.** `raise ValueError(f"invalid port: {port}")`
  not `raise ValueError("invalid")`.

## Other principles

### DRY — Don't Repeat Yourself

Every piece of knowledge should have one representation. But:

- **Rule of Three:** first time, write it. Second time,
  tolerate the duplication. Third time, extract. Premature
  abstraction is worse than duplication.
- **Don't abstract too early:** the right abstraction emerges
  after the third use, when the pattern is clear.
- **DRY applies to knowledge, not code:** two identical lines
  that represent different concepts are not a DRY violation.

### KISS — Keep It Simple, Stupid

The simplest code that works is the best code. Complexity must
earn its place:

- A design pattern that solves a problem you don't have is
  complexity without benefit.
- A clever one-liner that requires a comment is worse than
  three obvious lines.
- "Simple" does not mean "short." It means easy to understand.

### YAGNI — You Aren't Gonna Need It

Do not build for hypothetical future requirements. Build what
you need now. When the future arrives and you need it, you will
understand the requirement better than you do today.

- No "just in case" parameters.
- No "configurable" that is never configured.
- No abstraction for one use.

### Law of Demeter (Tell, Don't Ask)

> A method should only call methods on: itself, its
> parameters, its own fields, objects it creates.

Do not reach through an object to get at its internals:

```python
# Bad: reaching through layers (train wreck).
total = order.get_customer().get_wallet().get_balance()

# Good: tell the object what you want.
total = order.get_available_balance()
```

The difference: in the good version, `order` knows how to
compute its available balance. In the bad version, the caller
knows the internal structure of order → customer → wallet.

### Composition over inheritance

Prefer composing objects over inheriting from them. Inheritance
is the strongest coupling in OOP; composition is more flexible.

```python
# Bad: inheritance for code reuse.
class Stack(list):  # inherits all of list's methods
    def push(self, item): self.append(item)
    def pop(self): return super().pop()
# Stack now has insert, remove, sort, etc. — none make sense.

# Good: composition.
class Stack:
    def __init__(self):
        self._items = []
    def push(self, item): self._items.append(item)
    def pop(self): return self._items.pop()
    def is_empty(self): return len(self._items) == 0
```

**When inheritance is right:** when there is a genuine
"is-a" relationship (a `Dog` is an `Animal`) and the subclass
honors the Liskov contract.

## Applying the principles: a review checklist

When reviewing code, check in this order:

1. **Fail fast:** Are inputs validated at the boundary?
2. **Single Responsibility:** Does each unit have one reason
   to change?
3. **Null safety:** Are nulls handled explicitly?
4. **Error handling:** Are exceptions specific, with context,
   and not swallowed?
5. **Defensive copying:** Do mutable objects stay inside their
   owner?
6. **Tell, Don't Ask:** Does the caller reach through layers?
7. **DRY / Rule of Three:** Is there unjustified duplication?
   Is there premature abstraction?
8. **KISS / YAGNI:** Is there complexity that does not earn
   its place?
9. **Open/Closed:** Can new behavior be added without editing
   existing code?
10. **Dependency Inversion:** Do high-level modules depend on
    abstractions?

## Integration with library agents

- `architecture-validator`: checks these principles at the
  system level (components, services, layers). This skill is
  the code-level complement.
- `code-reviewer`: apply this checklist during code review.
- `implementer`: apply these principles when writing code.
- `architect`: design with these principles at the module
  level.
- `debugger`: defensive programming prevents the bugs you
  debug.

## Integration with library skills

- `/ma-dev-workflow` — these principles apply within any
  development workflow (spec, TDD, BDD).
- `/ma-test-methodologies` — TDD and property-based testing
  are natural complements to defensive programming.
- `/ma-legacy-testing` — Dependency Inversion (D in SOLID) is
  the same as seam-based dependency injection. Use this skill
  to create the seams that `/ma-legacy-testing` needs.
- `/ma-modernize` — applying these principles during
  modernization improves the target system's design.

## Sources

- Robert C. Martin, *Clean Code* (Prentice Hall, 2008) —
  SOLID, KISS, DRY, Tell Don't Ask, fail-fast.
- Robert C. Martin, *Agile Software Development: Principles,
  Patterns, and Practices* (Prentice Hall, 2002) — SOLID
  principles origin.
- Steve McConnell, *Code Complete* (Microsoft Press, 2004) —
  defensive programming, defensive copying, assertions.
- Andy Hunt & Dave Thomas, *The Pragmatic Programmer*
  (Addison-Wesley, 1999) — DRY, YAGNI, Law of Demeter.
- Michael Feathers, *Working Effectively with Legacy Code*
  (Prentice Hall, 2004) — seams and dependency inversion for
  legacy code.
