# RabbitMQ broker contract

Attaches alongside `messaging.md`. AMQP work-queue broker: routing is
the design, acknowledgment is the contract.

## Eras

Classic queues versus modern quorum queues: quorum queues are the
durability default for new work; classic mirrored queues are the
legacy being replaced, and stream queues exist for the log-shaped
use case. The declarations name the era.

## Idiom

- Topology is the design: exchanges, queues, bindings — declared
  idempotently by clients, versioned with the code.
- Manual acknowledgment after the work, requeue with a retry limit;
  publisher confirms on the producer side.
- Prefetch is the backpressure dial: bounded per consumer, never
  unbounded.

## Structure

- Dead-letter exchanges named per queue, TTL where staleness is a
  policy — the core's dead-letter discipline, native here.
- Transactions avoided: confirms and acks carry the guarantees at
  a fraction of the cost.

## Pitfalls

- Auto-ack consumers: at-most-once wearing a fast costume.
- Unbounded queues behind a stopped consumer — disk is the limit,
  then the outage.
- Requeue storms: one poison message looping forever without a
  retry count.
- Different clients declaring different topology: the mismatch is a
  runtime error by design, silently fatal by accident.
