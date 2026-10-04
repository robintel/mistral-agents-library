# Dialects

Contracts live in role folders: `languages/` (idiom floors and the
contract language graphql), `engines/` (the sql core and its engine
contracts), `stores/` (the nosql core and its store contracts),
`brokers/` (the messaging core and its broker contracts),
`platforms/` (hadoop, spark), `patterns/` (etl, attached by the shape
of the work). Cores live with their families; conservation is a
status in a contract's header, not a folder. One file per language,
engine, store, broker, or pattern: agents attach a dialect to a task
the way they attach any other context.

## Authoring a dialect

- Concrete rules, never exhortation. "Never bare `except:`" changes output;
  "write elegant code" changes nothing. A rule a reader cannot check does
  not belong here.
- The dialect extends the elegance bar in `../standards.md`; it never
  restates it. Cross-language rules live there, once.
- Sections: Idiom, Structure, Errors, Testing, Dependencies, Starting
  from scratch, Pitfalls. Keep the file under ~40 lines — every line is
  paid again as context on every code task.
- Eras: assume a language has eras until proven otherwise — Python 2
  versus 3, Rust editions, Go version thresholds, CommonJS versus
  ESM, Java 8 versus 21, fixed-form versus free-form Fortran. One
  Eras or Form section maps them, and the build names the era
  (`python_requires`, Cargo.toml edition, go.mod, tsconfig, pom,
  csproj). Write the era you find; modernizing is its own brief,
  never a ride-along.
- Two kinds of dialect: modern languages get idiom floors; legacy
  languages (fortran, cobol, classic VB) get conservation contracts —
  preservation over modernization, the running system is the spec, the
  regression baseline captured before any change.
- Status: a dialect never validated against a real codebase is marked
  experimental in its header. Agents treat its rules as provisional
  and flag findings that depend on them for human review.
- SQL is two-layer: `sql.md` is the vendor-neutral core; engine
  contracts (`postgres`, `mysql`, `oracle`, `bigquery`, `sqlite`,
  `sqlserver`, `snowflake`) attach alongside it and extend it, never
  restate it. Engine files carry their own Eras where eras are real —
  Oracle 10/11/12c, MySQL 5.7/8.0, SQL Server compatibility levels —
  and none where they are not, as the assume-eras rule requires both
  directions. A new engine is one file.
- NoSQL is two-layer with a thin core: the stores share no language,
  so `nosql.md` carries the modeling discipline — access-pattern-
  first, denormalization, consistency as a dial — and store contracts
  (`cassandra`, `mongodb`, `redis`, `hbase`, `elasticsearch`,
  `dynamodb`) attach alongside with the idiom and traps. The legacy
  mainframe stores (`ims`, `vsam`, `idms`, `adabas`, `cache-iris`) are
  conservation contracts in the same folder: experimental status,
  standalone attach — the nosql core descends from disciplines these
  stores invented, not the other way around.
- Messaging is two-layer like NoSQL: `messaging.md` carries the
  shared delivery semantics — the guarantees vocabulary, idempotent
  consumers, dead-lettering, replay policy — and broker contracts
  (`kafka`, `rabbitmq`, `sqs`, `ibm-mq`, `solace`, `activemq`,
  `nats`) attach alongside with the idiom and traps. Legacy brokers
  are not conservation contracts: IBM MQ and Solace are alive,
  maintained, and running production — they get the same treatment
  as the modern ones, with their eras named.
- Hadoop, Spark, and Kafka are platforms, not stores: their contracts
  cover the storage discipline, the compute engine, and the event
  log respectively — with Kafka attaching under the messaging core
  as a broker.
- GraphQL is a contract-language dialect: schema-first, thin
  resolvers, partial-error responses — attached alongside the
  implementation language's contract for schema and resolver work.
- ETL/ELT is a pattern contract, a different kind: attached by the
  shape of the work — the data-engineer's pipeline briefs — rather
  than by language. Idempotency is the law; T-placement is a priced
  decision; backfill is a designed capability, never a script.
- Precedence: the repo's conventions win; this contract is the floor; the
  Starting from scratch section pins the defaults when the repo is silent.
