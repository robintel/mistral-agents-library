# Lua dialect

Baseline style for Lua work. The repo's pinned conventions win on
conflict; when the repo is empty or silent, the Starting from scratch
section supplies the defaults.

## Eras

Lua 5.1 (the game-modding and embedded era: WoW addons, Garry's Mod,
OpenResty), Lua 5.2/5.3/5.4 (the modern era: integer subtype in 5.3,
to-be-closed variables, integer division, and goto in 5.4), and
LuaJIT (the performance era: game engines, high-throughput
networking, still on 5.1 semantics). The repo declares which;
LuaJIT is 5.1 with extensions — do not use 5.2+ features in
LuaJIT code. Neovim's embedded Lua is 5.1/LuaJIT. Nginx OpenResty
is LuaJIT. Roblox uses Luau, a gradually-typed derivative of
Lua 5.1 — not standard Lua.

## Idiom

- Tables are the only data structure: arrays are tables with
  1-based integer keys, objects are tables with string keys,
  classes are tables with metatables. Do not invent a second
  data structure.
- 1-based indexing: `array[1]` is the first element. Porting
  0-based logic from C/Python silently shifts every index.
- Local by default: `local x` unless the variable must be global.
  Globals are the namespace pollution of Lua — they are visible
  everywhere and collide silently.
- Metatables for operator overloading and OOP: `__index`,
  `__newindex`, `__call`, `__tostring`. One metatable per class,
  set once at class definition, never mutated per-instance.
- Coroutines for cooperative concurrency: `coroutine.create`,
  `coroutine.yield`, `coroutine.resume`. No preemptive threads
  in standard Lua — the C host owns the scheduler.
- `nil` is the only falsey value besides `false`: `0` and `""`
  are truthy. Test with `== nil`, not `not x`, when absence
  matters.

## Structure

- One module per file: `local M = {} ... return M` (the module
  pattern). No globals for module state.
- `require` returns the module table; cache is built-in, do not
  re-implement it.
- OOP is convention, not syntax: `function Class:method()` is
  sugar for `function Class.method(self)`. The colon is load-bearing.

## Errors

- `pcall`/`xpcall` for protected calls; `error()` raises,
  `assert()` guards. No exceptions — errors are return values
  through `pcall`.
- `xpcall` with a message handler for stack traces; bare `pcall`
  loses the traceback.
- Never `error()` without a level argument — the default blames
  the wrong line.

## Testing

- `busted` (BDD-style, most common) or `luaunit` (xUnit-style).
  Run with `busted` or `lua test_file.lua`.
- No standard test runner in the language itself.

## Dependencies

- LuaRocks (`luarocks`) for packages; pin in a `rock` file or
  lockfile. No `package.json` equivalent — the ecosystem is
  LuaRocks or vendored source.
- C modules: `require` loads `.so`/`.dll`; the FFI (LuaJIT) or
  `luaL_newlib` (5.2+) for bindings. Prefer pure-Lua when
  performance allows.

## Starting from scratch

- Lua 5.4 for new projects, LuaJIT when the host provides it
  (Neovim, OpenResty, game engine).
- `busted` for tests, LuaRocks for deps, `stylua` for formatting.
- No classes unless the domain needs them: plain functions and
  tables first.

## Pitfalls

- Global variables by accident (forgotten `local`): silent,
  cross-file, invisible until production.
- 0-based index from ported code: off-by-one on every loop.
- `#` operator on tables with holes (nil gaps): undefined length.
- Modifying a table while iterating with `pairs`: undefined order,
  possible skips. Collect keys first, then iterate.
- `tostring` on tables: memory address, not content. Use a
  serializer for debugging.
- Integer/float coercion pre-5.3: all numbers are doubles.
  Integer overflow wraps silently.
- C module ABI mismatch: LuaJIT FFI vs. standard `luaL_newlib`
  are incompatible.
