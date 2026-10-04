# IMS DB store contract

**Status: experimental and conservation** — never validated against a
production IMS estate; findings get practitioner review. A
conservation contract: attaches standalone; the nosql core descends
from disciplines this store invented.

IBM's hierarchical database (1966) — core banking and insurance to
this day. The hierarchy is the access path: DL/I calls walk segments
rooted at a parent, and the program's view (the PSB) is code.

## Preservation over modernization

- The DBD and PSB are code: database descriptions and program views,
  versioned like any source, changed with plans and baselines.
- Batch windows are contracts: checkpoint and restart designed, not
  hoped for. Capture regression baselines from job output before any
  change — the cobol contract's law, applied here.

## Idiom

- Positioning is the discipline: GU establishes position; GN and GNP
  walk from it; every read names its segment path. Unqualified
  walking is a full scan wearing a loop.
- GNP stays within the established parent: the twin-segment loop is
  the idiom.
- The organization (HISAM, HDAM, HIDAM) decides the access style; the
  DBD names what the program may assume.

## Pitfalls

- Position bugs: GN results depend on the last call — state, not
  syntax.
- A failed batch run left partial updates: checkpoint/restart is the
  design, not the recovery.
- Secondary indexes and logical relationships change DL/I path
  assumptions — schema migrations, never ride-alongs.
- Lock hold times in online regions are the throughput story.
