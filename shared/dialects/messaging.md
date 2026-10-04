# Messaging core

Attaches alongside a broker contract (kafka, rabbitmq, sqs, ibm-mq,
solace, activemq, nats). Brokers share no API — they share delivery
semantics, and every one of them demands the same consumer-side law.

## The vocabulary (decide, then say it)

- Delivery guarantees: at-most-once (loss possible, duplication not),
  at-least-once (duplication possible, loss not), exactly-once
  (neither — priced in complexity, configured, never assumed). Every
  integration states its guarantee in the design.
- Ordering: per queue, per partition, per key — never global; the
  unit of order is the unit of concurrency.
- Consumers are idempotent: the etl contract's law, imported whole —
  at-least-once means the consumer, not the broker, carries the
  correctness.

## The disciplines

- Dead-lettering is a designed capability from day one: poison
  messages land somewhere observable, reason attached, someone
  alerted. The alternative is a crash loop on one bad message.
- Backpressure is a contract: bounded queues with a stated full
  behavior — block, reject, or spill — never unbounded hope.
- Replay is a policy: how far back, and what a reprocessed message
  does. Designed before the first incident, not during it.
- Message schemas are contracts at the boundary: the serialization
  rules apply per message; evolution is versioned and compatible.

## Pitfalls (shared)

- Treating the broker as a database: queues drain, logs retain —
  know which one the system is built on.
- Silent consumer death: liveness is monitored, or nobody knows the
  system stopped.
- Guaranteed delivery promised by the producer, consumed
  at-most-once by the consumer — the mismatch nobody wrote down.
