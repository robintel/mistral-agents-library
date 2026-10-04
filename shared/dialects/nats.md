# NATS broker contract

Attaches alongside `messaging.md`. The lightweight end of the
spectrum: subjects, at-most-once core, and persistence (JetStream)
added with contracts rather than magic.

## Eras

Core NATS versus JetStream — often both in one system, so the era is
per-integration and stated every time: core is at-most-once, no
persistence, fast and honest; JetStream adds streams with retention,
acknowledgments, and replay for anything that must not be lost.

## Idiom

- Subjects are hierarchical with wildcards: the space is the API —
  designed like a namespace, consumed by intent.
- Core NATS requires a running subscriber to receive: the bus-model
  honesty; JetStream for loss that is unacceptable.
- JetStream streams: retention and limits decided per stream — max
  age, count, bytes; interest-based versus limits-based retention —
  the replay window is the contract.

## Structure

- Durable consumers carry their own guarantees: ack wait and max
  deliver are the retry and dead-letter story — set both, per the
  core.

## Pitfalls

- Publishing to core NATS with nobody listening: success, silently.
- Mixing models: queue groups in core NATS versus durable consumers
  in JetStream — the distributing logic differs, and confusion is
  duplicated delivery or dropped delivery.
- Max deliver unset: the poison-message loop with a modern accent.
- Subject collisions after wildcards: a namespace designed cheaply
  and paid for at scale.
