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
- Eras: when idiom is era-specific — Java 8 versus 21, fixed-form
  versus free-form Fortran, .NET Framework versus .NET 8 — one Eras or
  Form section maps them, and the build file names the era. Write the
  era you find; modernizing is its own brief, never a ride-along.
- Two kinds of dialect: modern languages get idiom floors; legacy
  languages (fortran, cobol, classic VB) get conservation contracts —
  preservation over modernization, the running system is the spec, the
  regression baseline captured before any change.
- Status: a dialect never validated against a real codebase is marked
  experimental in its header. Agents treat its rules as provisional
  and flag findings that depend on them for human review.
- Precedence: the repo's conventions win; this contract is the floor; the
  Starting from scratch section pins the defaults when the repo is silent.
