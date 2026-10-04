# Dialects

One file per language: the language-specific floor for code quality. Agents
attach a dialect to a task the way they attach any other context.

## Authoring a dialect

- Concrete rules, never exhortation. "Never bare `except:`" changes output;
  "write elegant code" changes nothing. A rule a reader cannot check does
  not belong here.
- The dialect extends the elegance bar in `../standards.md`; it never
  restates it. Cross-language rules live there, once.
- Sections: Idiom, Structure, Errors, Testing, Dependencies, Starting
  from scratch, Pitfalls. Keep the file under ~40 lines — every line is
  paid again as context on every code task.
- Precedence: the repo's conventions win; this contract is the floor; the
  Starting from scratch section pins the defaults when the repo is silent.
