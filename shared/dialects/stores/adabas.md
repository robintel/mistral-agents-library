# ADABAS store contract

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Attaches
standalone.

Software AG's inverted-list database (1971), usually with Natural as
its language — an estate shape common across European enterprises and
governments, still supported.

## Idiom

- Descriptors are the access paths: fields marked as descriptors
  (and multi-field superdescriptors) are what reads can seek on — a
  query on a non-descriptor is a physical scan, priced at file size.
- The ISN is the record's identity: reads by ISN, by descriptor value,
  or in physical order — three disciplines, chosen per access.
- The holding queue is the transaction: records held across commands
  until end-of-transaction or backout — hold times are the
  concurrency story.

## Preservation over modernization

- DDMs (the Natural data views) are code: versioned with the
  programs, changed with plans, baselines from job output.

## Pitfalls

- Write amplification: every updated descriptor costs the inverted
  lists — heavily-indexed files pay at update what they save at read.
- Long transactions degrade the whole database's concurrency: the
  holding queue is shared.
- ISN gaps and reuse: internal sequence is storage, never an
  application identifier.
- Field redefinitions and null-value representation: the layout is
  a contract, like a copybook.
