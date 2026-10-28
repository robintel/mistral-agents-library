# Lisp dialect

Baseline style for Lisp work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Eras

Four families share the name but not the discipline: Common Lisp
(ANSI CL, the standard, SBCL/CCL/LispWorks), Scheme (R5RS/R6RS/R7RS,
minimalist, Racket/Scheme48/Guile), Clojure (JVM, immutable data
structures, JVM interop), and Emacs Lisp (editor-centric, dynamic
scope, single namespace). The repo declares which; do not mix idioms
across families. Modernizing between families is a migration brief.

## Idiom

- Prefix notation everywhere: `(function arg1 arg2)`, not
  `function(arg1, arg2)`. Parentheses are the syntax; indentation
  is for humans, structure is for the reader.
- Macros are code that writes code: use them to extend the language
  for the domain, not to save keystrokes. A macro without a
  docstring is a bug.
- Functions are first-class: `mapcar`/`map` over explicit loops,
  `lambda` over named stubs, higher-order functions over callbacks
  with mutable state.
- Immutability by default (Clojure): persistent data structures,
  no `set!`/`setf` without a stated reason. Common Lisp and Emacs
  Lisp are mutable-first: mutation is explicit and scoped.
- No loop constructs in Scheme/Clojure: recursion and `reduce` over
  `do`/`while`. Common Lisp: `loop` macro is idiomatic, `do` is
  legacy.

## Structure

- One package/namespace per file (Common Lisp: `defpackage` +
  `in-package`; Clojure: `ns`; Scheme: `define-library`).
- Public API at the top; internals below a visible boundary.
- REPL-driven development: code is loaded incrementally, not
  compiled whole. The REPL session is part of the workflow.

## Errors

- Common Lisp: conditions and restarts (`handler-case`,
  `restart-case`) — the error boundary is a first-class control
  structure, not a catch block.
- Clojure: `ex-info` with structured data, `try/catch` at the
  boundary. Never swallow exceptions.
- Scheme: `guard` (R7RS) or `with-exception-handler`. R5RS has
  no standard error handling — the implementation's wins.

## Testing

- Common Lisp: FiveAM or Prove. Clojure: `clojure.test` or Kaocha.
  Scheme: SRFI-64 (`test-*` forms). Emacs Lisp: ERT.
  Tests run from the REPL or CI; both are valid.

## Dependencies

- Common Lisp: Quicklisp + `qlfile` or ASDF system definition.
- Clojure: `deps.edn` (CLI) or `project.clj` (Leiningen).
- Scheme: implementation-specific; Racket uses `#lang` and
  `raco pkg`.

## Starting from scratch

- Common Lisp: SBCL, ASDF, Quicklisp, Prove.
- Clojure: `deps.edn`, `clojure.test`, no Leiningen unless the
  repo already uses it.
- Scheme: Racket for new projects, R7RS-small otherwise.
- Emacs Lisp: `package.el`, ERT, no external deps for editor code.

## Pitfalls

- Macros that capture variables unintentionally (gensym hygiene).
- `eval` used where a macro or higher-order function was meant.
- Deep recursion without tail-call optimization (Scheme
  guarantees TCO; Common Lisp does not).
- Mixing families: `cl-` prefixed symbols in Clojure, `defn`
  in Common Lisp.
- Mutable global state in Clojure (`def` at the top level) —
  use `defonce` or atoms.
- Emacs Lisp dynamic scope leaking across function boundaries.
